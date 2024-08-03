# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 16:31
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : common.py
# @Software: PyCharm

from app.models.llm.models import LLMCategory


async def query_llm_category(category_id) -> (bool, LLMCategory):
    """查询LLM分类"""

    llm_category = await LLMCategory.get_or_none(id=category_id)
    if not llm_category:
        return False, None
    else:
        return True, llm_category
