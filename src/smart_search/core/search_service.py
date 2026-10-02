from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from smart_search.models.schemas import SearchCondition, ProductRecommendResponse
from smart_search.config.tools import tools
from smart_search.config.prompts import prompt
import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        # 获取大语言模型
        self.llm = tools.get_model()
        # 获取Prompt
        self.search_extract_prompt = prompt.SEARCH_EXTRACT_PROMPT
        self.search_prompt = prompt.SEARCH_PROMPT
        # 创建向量检索实例
        self.vector_store = tools.get_vector_store()
        # 创建搜索记忆检索索引
        self.checkpointer = InMemorySaver()
        @tool
        def vector_search_tool(query: str) -> str:
            """
            商品向量检索工具，获取相关商品资料。
            Args:
                query: 用户问题
            return: 商品信息列表
            """
            print(f"vector_search_tool: query={query}")
            docs = self.vector_store.similarity_search(query, k=10)
            return "\n".join([f"{doc.page_content} | meta:{doc.metadata}" for doc in docs])

        self.vector_search_tool = vector_search_tool

    # 用户查询 - 搜索条件结构化提取
    async def extract_search_condition(self,query:str) -> SearchCondition:
        """
        商品搜索条件结构化提取
        :param query: 用户问题
        :return: SearchCondition对象
        """
        # 1. 构建Pydantic解析器
        parser = PydanticOutputParser(pydantic_object=SearchCondition)

        # 2. 构建Prompt模板
        prompt = ChatPromptTemplate.from_messages([
            ("system",  self.search_extract_prompt),
            ("human", "用户查询：{query}")
        ]).partial(format_instructions=parser.get_format_instructions())

        # 3. 组装执行链路
        extract_chain = prompt | self.llm | parser
        result = await extract_chain.ainvoke({"query": query})
        return result   
    
     # 商品推荐
    async def recommend_product(self, query: str, thread_id=0):
  
        # 1. 先提取搜索条件
        condition = await self.extract_search_condition(query)
        logger.info(f"提取的条件: keyword={condition.keyword}, price={condition.min_price}-{condition.max_price}")
        
        # 2. 构建搜索查询（使用 keyword）
        search_query = condition.keyword if condition.keyword else query
        
        # 3. 直接使用向量搜索（不通过 Agent）
        docs = self.vector_store.similarity_search(search_query, k=20)
        logger.info(f"向量搜索返回 {len(docs)} 条结果")
        
        # 4. 按价格过滤
        filtered_docs = []
        for doc in docs:
            price = doc.metadata.get('price', 0)
            if condition.min_price <= price <= condition.max_price:
                filtered_docs.append(doc)
        
        logger.info(f"价格过滤后剩余 {len(filtered_docs)} 条结果")
        
        # 5. 如果没结果，返回空
        if not filtered_docs:
            return ProductRecommendResponse(
                summary="暂无符合您条件的商品",
                product_list=[],
                reason=["知识库中未找到匹配的商品，请调整搜索条件"]
            )
        
        # 6. 构建商品列表
        from smart_search.models.schemas import GoodsInfo
        product_list = []
        for doc in filtered_docs[:10]:
            meta = doc.metadata
            product_list.append(GoodsInfo(
                id=meta.get('id'),
                spu_id=meta.get('spu_id'),
                sku_name=meta.get('sku_name'),
                price=meta.get('price'),
                sku_default_img=meta.get('sku_default_img')
            ))
        
        # 7. 生成推荐理由
        # 使用 LangChain Agent 生成推荐理由（简化版）
        from langchain_core.messages import SystemMessage, HumanMessage
        
        prompt_template = f"""
        用户查询：{query}
        搜索条件：关键词={condition.keyword}，价格范围={condition.min_price}-{condition.max_price}元
        
        推荐商品列表：
        {chr(10).join([f"- {p.sku_name}（{p.price}元）" for p in product_list])}
        
        请生成：
        1. summary：一段简短的总结导语
        2. reason：3-5条推荐理由
        
        直接返回JSON格式，不要其他文字。
        """
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content="你是专业的商品推荐助手"),
                HumanMessage(content=prompt_template)
            ])
            
            import json
            result = json.loads(response.content)
            
            return ProductRecommendResponse(
                summary=result.get("summary", f"为您推荐以下{condition.keyword}商品"),
                product_list=product_list,
                reason=result.get("reason", ["这些商品符合您的需求"])
            )
        except Exception as e:
            logger.error(f"生成推荐理由失败: {e}")
            return ProductRecommendResponse(
                summary=f"为您推荐以下符合条件的{condition.keyword}商品",
                product_list=product_list,
                reason=[f"价格在{condition.min_price}-{condition.max_price}元之间的商品"]
            )