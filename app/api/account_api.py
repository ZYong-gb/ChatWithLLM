from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel  # 数据验证模型
from sqlalchemy.ext.asyncio import AsyncSession  # 异步数据库会话
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.database.database import db_dependency
from app.models.dify_models_ORM import Agent, User
from app.database.database import db_dependency
from app.schemas.account_schemas import UserRegisterRequest, UserLoginRequest
from app.service.account_serve import UserService


login_router = APIRouter()



# ===== 用户注册接口 =====
@login_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterRequest, db: db_dependency):
    """
    用户注册接口
    
    Args:
        user_data: 用户创建请求数据
        db: 数据库会话依赖
        
    Returns:
        dict: 注册成功的响应消息
    """
    user_dict = user_data.dict()  # 将Pydantic模型转换为字典
    return await UserService.register_user_def(db, user_dict)



# ===== 用户 login 接口 =====
@login_router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(user_data: UserLoginRequest, db: db_dependency):
    """
    用户注册接口
    
    Args:
        user_data: 用户创建请求数据
        db: 数据库会话依赖
        
    Returns:
        dict: 注册成功的响应消息
    """
    user_dict = user_data.dict()  # 将Pydantic模型转换为字典
    return await UserService.login_user_def(db, user_dict)



# ===== 用户 delete 接口 =====
@login_router.delete("/delete", status_code=status.HTTP_201_CREATED)
async def delete_user(user_data: UserLoginRequest, db: db_dependency):
    """
    用户注册接口
    
    Args:
        user_data: 用户创建请求数据
        db: 数据库会话依赖
        
    Returns:
        dict: 注册成功的响应消息
    """
    user_dict = user_data.dict()  # 将Pydantic模型转换为字典
    return await UserService.delete_user_def(db, user_dict)
