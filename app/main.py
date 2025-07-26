from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles

# from app.api.test_2 import router2 as test2
# from app.api.dify_chat_api import dify_router
from app.api.operate_dify_api import dify_router
from app.api.account_api import login_router


app = FastAPI()

# 配置CORS，以便跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册静态文件路由
# app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册API路由
# app.include_router(test_router, prefix="/api")
# app.include_router(test2,prefix="/api",tags=["打打怪"])
app.include_router(dify_router, prefix="/api", tags=["Dify_api"])
app.include_router(login_router, prefix="/user", tags=["账户"])


@app.get("/")
async def root():
    return {"message": "测-2025-07-05 11:45"}
