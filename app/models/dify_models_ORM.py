from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, func, JSON,text,ForeignKey
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import false  # 导入 false 表达式


# 定义 ORM 基类
Base = declarative_base()



# 数据库表形式

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(250), unique=True, nullable=False)
    user_account = Column(String(255), unique=True,nullable=False) 
    user_password = Column(String(255), nullable=False)  # 使用字符串存储密码哈希
    user_VIP = Column(Boolean,default=False, nullable=False)  # 使用整数0表示false
    user_VIP_deadline = Column(DateTime, nullable=True)  
    # 添加创建时间字段
    created_at = Column(DateTime, server_default=func.now())  # 数据库层默认值,server_default=func.now()，由数据库自动生成插入时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    owner_agents = Column(JSON, nullable=True)  # 使用JSON类型存储列表


class Agent(Base):
    __tablename__ = 'dify_agent'

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), unique=False, nullable=False) 
    agent_describe = Column(Text, nullable=True, )
    agent_url = Column(String(255), nullable=False)
    agent_api_key = Column(String(500), nullable=False)
    agent_Content_Type = Column(String(50),default='application/json')
    response_mode = Column(String(50),default="blocking")
    user = Column(String(255),unique=True, nullable=False)
    # conversation_id = Column(String(36), nullable=True)
    auto_generate_name = Column(Boolean,default=True)
    created_at = Column(DateTime, server_default=func.now())  # 数据库层默认值,server_default=func.now()，由数据库自动生成插入时间
    belong_user_account = Column(String(255), unique=False, nullable=False)
