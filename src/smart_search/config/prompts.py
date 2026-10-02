class Prompt:
    def __init__(self):
        self.SEARCH_EXTRACT_PROMPT =  """
        你是商品搜索条件提取助手，根据用户查询提取商品筛选条件。
        需要提取的参数：
        1. keyword: 搜索关键词
        2. min_price: 最低价格,若没有提取到值，min_price=0
        3. max_price: 最高价格,若没有提取到值，max_price=100000
        示例：
        查询："我想买一个2000-4000元的小米手机"
        返回：{{"keyword": "小米手机", "min_price": 2000, "max_price": 4000}}
        只输出JSON，不要额外文字: {format_instructions}"""

        self.SEARCH_PROMPT = """
        请严格依据上下文内真实信息回答用户问题，**严禁编造不存在的商品信息**。
        规则要求：
        1. 根据用户问题调用vector_search_tool工具检索商品知识库，返回的商品信息生成上下文；
        2. 仅使用上下文存在的数据进行商品推荐，并给出推荐理由品；
        3. 若上下文没有匹配内容：summary="暂无相关信息"，product_list=[]，reason=[]；
        4. 输出格式必须是纯粹标准JSON，禁止附带Markdown、```json、注释、前言、总结等任何额外文本；
        5. 严格遵循输出字段结构，不随意增删字段。
        """

prompt = Prompt()
