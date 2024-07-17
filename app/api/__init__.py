# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 14:33
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm


from fastapi import APIRouter

from app.api.chat_ws.chat_ws import chat_ws_router

api = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={
        404: {"description": "Not found"}
    },
)

# 一级路由
admin = APIRouter(prefix="/admin", tags=["后台"])
front = APIRouter(prefix="/front", tags=["前台"])

# 二级路由
chat_uri = APIRouter(prefix="/chat", tags=["助手"])

# 三级路由-后台
chat_uri.include_router(chat_ws_router, tags=["对话"])

# 统一注册
api.include_router(chat_uri)
