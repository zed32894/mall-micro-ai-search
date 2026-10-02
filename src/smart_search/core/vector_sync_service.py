import logging
import hashlib
import tiktoken
from langchain_community.utilities import SQLDatabase
from langchain_community.document_loaders import SQLDatabaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from smart_search.config.tools import tools

logger = logging.getLogger(__name__)

# 向量化配置常量
CHUNK_SIZE = 256
CHUNK_OVERLAP = 25
BATCH_SIZE = 100
TIKTOKEN_ENCODING = "cl100k_base"


def tiktoken_len(text: str) -> int:
    """tiktoken计算token长度"""
    tokenizer = tiktoken.get_encoding(TIKTOKEN_ENCODING)
    return len(tokenizer.encode(text))


class ProductVectorSyncService:
    def __init__(self):
        self.sql_engine = tools.get_sql_engine()
        self.vector_store = tools.get_vector_store()

    @staticmethod
    def custom_page_content_mapper(row) -> str:
        """将商品字段拼接为文档page_content"""
        fields = ["sku_name", "sku_attribute", "brand_name", "category_name","price"]
        content_parts = [str(getattr(row, field, "")) for field in fields]
        return "。".join(content_parts)

    @staticmethod
    def custom_metadata_mapper(row) -> dict:
        """把数据库行全部字段填充为文档metadata"""
        metadata = {}
        for key in row.keys():
            metadata[key] = getattr(row, key)
        return metadata

    @staticmethod
    def _generate_doc_id(doc: Document) -> str:
        """根据sku_id+chunk内容生成md5唯一文档id"""
        raw = f"{doc.metadata['id']}_{doc.page_content.strip()}".encode("utf‑8")
        return hashlib.md5(raw).hexdigest()

    def load_sku_from_mysql(self) -> str:
        """
        从MySQL读取SKU商品，流式分批写入Redis向量库
        :return: 执行结果信息字符串
        """
        db = SQLDatabase(self.sql_engine)
        sql_query = """
            SELECT id,spu_id,price,sku_name,sku_attribute,brand_name,category_name,sku_default_img
            FROM sku_info WHERE deleted=0
        """

        loader = SQLDatabaseLoader(
            query=sql_query,
            db=db,
            page_content_mapper=self.custom_page_content_mapper,
            metadata_mapper=self.custom_metadata_mapper,
        )
        # 懒加载数据，避免一次性加载所有数据到内存中
        doc_iterator = loader.lazy_load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", "，", " "],
            length_function=tiktoken_len,
            strip_whitespace=True
        )
       
        batch_docs: list[Document] = []
        total_chunk = 0
        # 分批次处理数据
        for doc in doc_iterator:
            chunk_texts = splitter.split_text(doc.page_content)
            for chunk in chunk_texts:
                chunk_doc = Document(page_content=chunk, metadata=doc.metadata.copy())
                batch_docs.append(chunk_doc)
                total_chunk += 1

                # 达到批次阈值，批量写入向量库
                if len(batch_docs) >= BATCH_SIZE:
                    doc_ids = [self._generate_doc_id(d) for d in batch_docs]
                    self.vector_store.add_documents(documents=batch_docs, ids=doc_ids)
                    logger.info(f"批量入库 {len(batch_docs)} 条，累计分片：{total_chunk}")
                    batch_docs.clear()

        # 处理剩余不足一整批的数据
        if batch_docs:
            doc_ids = [self._generate_doc_id(d) for d in batch_docs]
            self.vector_store.add_documents(documents=batch_docs, ids=doc_ids)
            logger.info(f"收尾入库 {len(batch_docs)} 条分片")

        result_msg = f"MySQL数据向量化入库完成！总分片数量：{total_chunk}"
        logger.info(result_msg)
        return result_msg
