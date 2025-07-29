from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.future import select  # 异步SQL查询

from app.models.dify_models_ORM import User
from app.core.hash_security import get_password_hash, verify_password


# ===== 工具函数：通过账号查询用户 =====
async def get_user_by_account(db: AsyncSession, account: str):
    result = await db.execute(select(User).where(User.user_account == account))
    user = result.scalars().first()  # 获取查询结果中的第一个用户
    return user


class UserService:
    @staticmethod
    async def register_user_def(db: AsyncSession, user_data: dict) -> dict:
        # 检查账号是否已存在
        existing_user = await get_user_by_account(db, user_data["user_account"])
        if existing_user:
            raise HTTPException(status_code=400, detail="账号已存在")
        
        # 创建用户对象
        hashed_password = get_password_hash(user_data["user_password"])
        db_user = User(
            user_name=user_data["user_name"],
            user_account=user_data["user_account"],
            user_password=hashed_password,
            owner_agents=[]  # 拥有的代理列表（初始为空）
        )
        
        # 数据库操作
        db.add(db_user)
        try:
            await db.commit()
            await db.refresh(db_user)
            return {"message": "用户注册成功", "user_account": db_user.user_account}
        except IntegrityError as e:
            await db.rollback()
            if "user_account" in str(e):
                raise HTTPException(status_code=400, detail="账号已存在")
            raise HTTPException(status_code=500, detail="数据库操作失败")
        except Exception as e:
            await db.rollback()
            # 实际项目中应使用logging模块记录日志
            print(f"注册失败: {str(e)}")
            raise HTTPException(status_code=500, detail="服务器内部错误")
        

    @staticmethod
    async def login_user_def(db: AsyncSession, user_data: dict):
        try:
            existing_user = await get_user_by_account(db, user_data["user_account"])
            if not existing_user:
                raise HTTPException(status_code=400, detail="账号不存在")
            # 验证明文密码与数据库中的哈希密码一致性
            password_is_correct = verify_password(
                plain_password = user_data["user_password"],
                hashed_password = existing_user.user_password
                )
            if not password_is_correct:
                raise HTTPException(status_code=400, detail="密码错误")
            
            return{
                "message":"登录成功",
                "user_account": existing_user.user_account,
                "user_name": existing_user.user_name,
            }
        except HTTPException as http_exc:  # 明确捕获HTTPException
            # 直接重新抛出HTTP异常
            raise http_exc
            
        except Exception as e:
            # 处理其他所有异常
            print(f"登录失败: {str(e)}")
            raise HTTPException(status_code=500, detail="服务器内部错误")
        


    @staticmethod
    async def delete_user_def(db: AsyncSession, user_data: dict):
        try:
            # 1. 检查用户是否存在
            existing_user = await get_user_by_account(db, user_data["user_account"])
            if not existing_user:
                raise HTTPException(status_code=400, detail="账号不存在")
            # 2. 验证密码
            password_is_correct = verify_password(
                plain_password=user_data["user_password"],
                hashed_password=existing_user.user_password
            )
            if not password_is_correct:
                raise HTTPException(status_code=400, detail="密码错误")
            # 3. 执行删除操作
            await db.delete(existing_user)
            await db.commit()
            return {"message": "用户删除成功"}
            
        except HTTPException as http_exc:
            # 直接重新抛出HTTP异常
            raise http_exc
        except Exception as e:
            # 回滚数据库事务
            await db.rollback()
            # 记录错误日志（生产环境应该使用logging模块）
            print(f"删除用户失败: {str(e)}")
            raise HTTPException(status_code=500, detail="服务器内部错误")
