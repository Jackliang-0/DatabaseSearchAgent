# 导入FastAPI核心类
import uuid

from fastapi import FastAPI,Request

from app.api.routers.query_router import query_router
from app.core.context import request_id_ctx_var
from app.core.lifespan import lifespan

# 创建FastAPI应用实例
app = FastAPI(lifespan=lifespan)

# 注册路由
app.include_router(query_router)

# 整合中间件->设置异步协程上下文变量
@app.middleware("http")
async def add_request_cxt_var(request: Request, call_next):
    # 设置异步协程上下文变量
    request_id_ctx_var.set(uuid.uuid4())
    return await call_next(request)
