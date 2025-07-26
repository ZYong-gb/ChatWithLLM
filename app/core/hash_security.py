# 导入必要的库和模块
from jose import JWTError, jwt  # JWT令牌处理库
from passlib.context import CryptContext  # 密码哈希库
from datetime import datetime, timedelta  # 日期时间处理
from app.core.config import dify_settings  # 假设这是你的配置模块（包含 AES_KEY）


# ===== 密码哈希工具 =====
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# CryptContext:这是 passlib 库中用于管理密码哈希策略的核心类,它提供了统一的接口来处理多种密码哈希算法,支持密码的哈希生成、验证和迁移
# schemes=["bcrypt"]: 指定使用的密码哈希算法为 bcrypt,一种专门为密码存储设计的加密算法
# deprecated="auto": 自动检测并标记过时的哈希算法, 当有更好的算法可用时，会自动标记旧算法为不推荐, 允许在验证旧密码后自动升级到新算法


#  生成密码哈希
def get_password_hash(password: str):
    return pwd_context.hash(password) 

# 验证哈希密码的一致性, 验证明文密码是否与哈希密码匹配
def verify_password(plain_password: str, hashed_password: str) ->bool:
    return pwd_context.verify(plain_password, hashed_password)



# # ===== JWT 工具函数,创建包含过期时间的JWT令牌=====
# def create_access_token(data: dict, expires_delta: timedelta = None):
#     """创建JWT访问令牌"""
#     # 复制传入的数据
#     to_encode = data.copy()  
#     # 计算令牌过期时间
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     # 添加过期时间到编码数据
#     to_encode.update({"exp": expire})  
#     # 使用JWT编码数据，生成令牌
#     encoded_jwt = jwt.encode(to_encode, dify_settings.Hash_KEY, algorithm=dify_settings.Hash_ALGORITHM)
#     return encoded_jwt