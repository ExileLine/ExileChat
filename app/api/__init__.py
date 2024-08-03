# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 14:33
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm


from fastapi import APIRouter

from app.api.admin_api.admin_login_api import admin_login_router
from app.api.llm_api.llm_category_api import llm_category_router
from app.api.llm_api.llm_api import llm_router
from app.api.able_api.able_api import able_router
from app.api.document_vector_api.document_vector_api import document_router
from app.api.chat_ws.chat_ws import chat_ws_router

# 一级路由
api = APIRouter(prefix="/api", tags=["api"], responses={404: {"description": "Not found"}})
ws = APIRouter(prefix="/ws", tags=["ws"])

# 二级路由
admin = APIRouter(prefix="/admin", tags=["后台"])
front = APIRouter(prefix="/front", tags=["前台"])

# 三级路由-后台
admin.include_router(admin_login_router, prefix="/login", tags=["Admin登录"])
admin.include_router(llm_category_router, prefix="/llm_category", tags=["LLM分类"])
admin.include_router(llm_router, prefix="/llm", tags=["LLM"])
admin.include_router(able_router, prefix="/able", tags=["后台能力"])
admin.include_router(document_router, prefix="/document", tags=["文档向量"])
front.include_router(able_router, prefix="/able", tags=["前台能力"])

# 统一注册
api.include_router(admin)
api.include_router(front)
ws.include_router(chat_ws_router, tags=["对话ws"])
