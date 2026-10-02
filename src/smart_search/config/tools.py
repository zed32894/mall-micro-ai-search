from smart_search.config.settings import settings
from langchain_core.embeddings import embeddings
import mysql.connector
from langchain_redis import RedisConfig
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_redis import RedisVectorStore
import redis
from sqlalchemy import create_engine

class Tools:
   
    # 获取MySQL连接
    def get_mysql_conn(self):
        return mysql.connector.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DB
        )
    # # 获取Redis连接  
    def get_redis_conn(self):
        return redis.Redis.from_url(
            url=settings.REDIS_URL,
            decode_responses=True,  # 自动将bytes解码为str，避免手动解码
            socket_timeout=5,       # 连接超时时间
            retry_on_timeout=True   # 超时重试
        )
   
    # 获取向量模型
    def get_embeddings(self):
        return OpenAIEmbeddings(
            base_url=settings.EMBED_BASE_URL, 
            api_key=settings.EMBED_API_KEY, 
            model=settings.EMBED_MODEL
        )
    # 获取大语言模型
    def get_model(self):
        return ChatOpenAI(
            base_url=settings.BASE_URL,
            api_key=settings.OPEN_API_KEY,
            model=settings.LLM_MODEL,
            temperature=0.1,
            extra_body={
                "enable_thinking": False
            }
        )
    # 获取向量库
    def get_vector_store(self):
        config = RedisConfig(
            index_name=settings.INDEX_NAME,
            redis_url=settings.REDIS_URL
        )
        return RedisVectorStore(
            embeddings=self.get_embeddings(),
            config=config
        )
    # 创建 SQLAlchemy 引擎
    def get_sql_engine(self):
        url = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
        return create_engine(url)
      
tools = Tools()
