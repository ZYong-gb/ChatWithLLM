# login_schemas.py - 数据验证层
from pydantic import BaseModel

class Token(BaseModel):
    """令牌响应模型"""
    access_token: str  # 访问令牌
    token_type: str    # 令牌类型（通常为"bearer"）


class UserRegisterRequest(BaseModel):
    """用户创建请求模型"""
    user_name: str      # 用户名
    user_account: str   # 用户账号
    user_password: str  # 用户密码


class UserLoginRequest(BaseModel):
    user_account: str
    user_password: str