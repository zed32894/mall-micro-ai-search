from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", # 注意会优先读取windows环境变量
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # MySQL
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    # Redis
    REDIS_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    # Embedding
    EMBED_BASE_URL: str
    EMBED_API_KEY: str
    EMBED_MODEL: str

    # LLM
    BASE_URL: str
    OPEN_API_KEY: str 
    LLM_MODEL: str

    # Redis向量索引名称
    INDEX_NAME: str 

settings = Settings()
