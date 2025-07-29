from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel
from app.models.dify_models_ORM import Agent, User
from sqlalchemy import select, exc



# 从数据库获取用户
async def get_user(db, user_account: str) -> User:
    result = await db.execute(select(User).where(User.user_account == user_account))
    return result


