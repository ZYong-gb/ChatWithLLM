from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.core.config import dify_settings



# 数据库连接 URL（假设 dify_settings 已正确定义）
DATABASE_URL = (
    f"mysql+aiomysql://{dify_settings.MYSQL_USER}:{dify_settings.MYSQL_PASSWORD}"
    f"@{dify_settings.MYSQL_HOST}:{dify_settings.MYSQL_PORT}/{dify_settings.MYSQL_NAME}"
)

# 创建异步引擎（推荐不手动指定 poolclass，SQLAlchemy 会自动选择合适的异步池）
async_engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=False
)

# 创建异步 Session 工厂
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 依赖项：获取异步数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# 依赖项类型标注（正确使用 AsyncSession）
db_dependency = Annotated[AsyncSession, Depends(get_db)]
