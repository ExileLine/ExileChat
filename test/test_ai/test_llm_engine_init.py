# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:28
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_llm_engine_only.py
# @Software: PyCharm

import asyncio

from fastapi.encoders import jsonable_encoder

from utils.ai.llm_engine import LLMEngine
from utils.db_connect import db_init_pg
from app.models.llm.models import LLM


async def main():
    """main"""

    await db_init_pg()

    llm = await LLM.get_or_none(id=4)
    print(jsonable_encoder(llm))

    llm_engine = LLMEngine(llm_example=llm)
    generated_message = await llm_engine.chat_only(prompt="你是强大的人工智能", input="你是谁?")
    print(generated_message)


if __name__ == "__main__":
    asyncio.run(main())
