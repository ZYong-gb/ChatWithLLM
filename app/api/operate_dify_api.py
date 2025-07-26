from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import select, exc
from app.database.database import db_dependency
from app.models.dify_models_ORM import Agent, User
# 导入 AES-GCM 加密函数
from app.core.aes_gcm_security import encrypt_aes_gcm_combined, decrypt_aes_gcm_combined


dify_router = APIRouter()


class CreateAgentRequest(BaseModel):
    agent_name: str
    agent_describe: str
    url: str
    api_key: str  # 接收明文API Key
    content_type: str = "application/json"
    response_mode: str = "blocking"
    # user: str = 'uuname1234'
    # conversation_id: str = None
    auto_generate_name: bool = True
    belong_user_account: str


class caht_llm(BaseModel):
    user: str
    query: str
    conversation_id: str


# 定义 Pydantic 模型用于映射数据库
class respose_chat_info(BaseModel):
    agent_url: str
    agent_api_key: str
    agent_Content_Type: str = "application/json"
    respose_mode: str = None
    user: str 
    conversation_id: str = None
    auto_generate_name: bool = None

    class Config:
        from_attributes = True



# 创建 Agent 
@dify_router.post("/dify_agents", status_code=status.HTTP_201_CREATED)
async def create_agent(request: CreateAgentRequest, db: db_dependency):
    # 验证必填字段
    if not all([request.agent_name, request.url, request.api_key, request.belong_user_account]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="缺少必填字段: agent_name, url, api_key 或 belong_user_account"
        )

    # 检查Agent名称是否已存在
    agent_name_result = await db.execute(select(Agent).where(Agent.agent_name == request.agent_name))
    if agent_name_result.scalar():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Agent名称已存在")

    try:
        # 使用组合加密方法
        combined_ciphertext = encrypt_aes_gcm_combined(request.api_key)

        # 生成默认user值
        user_value = f"user_{request.belong_user_account}_{datetime.utcnow().timestamp()}"

        db_agent = Agent(
            agent_name=request.agent_name,
            agent_describe=request.agent_describe,
            agent_url=request.url,
            agent_api_key=combined_ciphertext,
            agent_Content_Type=request.content_type,
            response_mode=request.response_mode,
            user=user_value,
            auto_generate_name=request.auto_generate_name,
            belong_user_account=request.belong_user_account,
            created_at = datetime.utcnow()
        )
        db.add(db_agent)
        await db.commit()
        await db.refresh(db_agent)
        return {"agent创建成功，agent_id为": db_agent.created_at}
    except exc.IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"数据完整性错误: {str(e)}. 可能是user值重复或必填字段缺失"
        )
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"加密失败: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建Agent失败: {type(e).__name__}: {str(e)}"
        )



# caht with Agent - 使用解密方法
@dify_router.post("/dify_agents/chat", status_code=status.HTTP_200_OK)
async def chat_agent(request: caht_llm, db: db_dependency):
    try:
        result = await db.execute(select(Agent).where(Agent.user == request.user))
        agent = result.scalars().first()
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent 未找到")
        
        # 解密逻辑 - 使用新的组合解密方法
        try:
            decrypted_key = decrypt_aes_gcm_combined(agent.agent_api_key)
            # 创建数据库表对象副本，避免直接修改ORM对象,即返回为此副本中数据
            agent_data = {
                "agent_url": agent.agent_url,
                "agent_api_key": decrypted_key,  # 使用解密后的密钥
                "agent_Content_Type": agent.agent_Content_Type,
                "respose_mode":  agent.response_mode,
                "user": agent.user,
                "conversation_id": request.conversation_id,
                "auto_generate_name": agent.auto_generate_name
            }
            chat_info_base = respose_chat_info(**agent_data)
            return chat_info_base
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"解密失败: {str(e)}"
            )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



# 查询所有 Agents - 不返回敏感API Key
@dify_router.get("/dify_agents", status_code=status.HTTP_200_OK)
async def read_agents(db: db_dependency):
    try:
        result = await db.execute(select(Agent))
        agents = result.scalars().all()
        
        # 返回不包含敏感API Key的数据
        safe_agents = []
        for agent in agents:
            safe_agents.append({
                "id": agent.id,
                "agent_name": agent.agent_name,
                "agent_describe": agent.agent_describe,
                "agent_url": agent.agent_url,
                "agent_Content_Type": agent.agent_Content_Type,
                "user": agent.user,
                "created_at": agent.created_at.astimezone().isoformat() if agent.created_at else None
            })
        
        return safe_agents
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 删除 Agent - 保持不变
@dify_router.delete("/dify_agents/{user}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(user: str, db: db_dependency):
    try:
        result = await db.execute(select(Agent).where(Agent.user == user))
        agent = result.scalar()
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent 未找到")
        await db.delete(agent)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return None
