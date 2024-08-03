# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 16:57
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : common.py
# @Software: PyCharm

from enum import Enum

from app.models.llm.models import LLM
from app.models.able.models import Able
from app.models.secretary.models import SecretaryCategory


async def query_secretary_category(category_id) -> (bool, SecretaryCategory):
    """查询助手分类"""

    secretary_category = await SecretaryCategory.get_or_none(id=category_id)
    if not secretary_category:
        return False, None
    else:
        return True, secretary_category


async def query_llm(llm_id) -> (bool, LLM):
    """查询llm"""

    llm = await LLM.get_or_none(id=llm_id)
    if not llm:
        return False, None
    else:
        return True, llm


async def query_able_list(ids) -> (bool, list[Able]):
    """查询能力列表"""

    able_list = await Able.filter(id__in=ids).all()
    if not able_list:
        return False, []
    else:
        return True, able_list


async def check_model_name(llm: LLM, model_name: str) -> bool:
    """检验`model_name`是否在这个`LLM`中"""

    if model_name not in [model.get("model") for model in llm.model_list]:
        return False
    return True


class AnswerMode(str, Enum):
    """应答模式"""
    free = 'free'
    stint = 'stint'
    compatible = 'compatible'
