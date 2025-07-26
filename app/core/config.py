from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# 加载环境变量（仅本地开发）
load_dotenv()


# 注意，环境变量(.env)中存在的值，在DifySetting这个类中也必须包含
class DifySetting(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_NAME: str
    
    APP_ENV: str = "dev"
    AES_KEY: str  # AES 密钥（Base64 编码）
    AES_GCM_NONCE_SIZE: int  
    
    Hash_KEY: str
    Hash_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    class Config:
        env_file =".env"
        env_file_encoding = "utf-8"

# 全局 AES-GCM 实例
dify_settings = DifySetting()
