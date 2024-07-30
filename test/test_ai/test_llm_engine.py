# -*- coding: utf-8 -*-
# @Time    : 2024/7/18 02:24
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_llm_engine.py
# @Software: PyCharm

import asyncio
from utils.ai.llm_engine import LLMEngine
from api_key import api_key


async def main():
    """main"""

    new_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key)

    new_engine.system_prompt = "你是一名Python专家"
    response_generator = new_engine.chat(input="Python是什么时候诞生的")

    async for chunk in response_generator:
        if isinstance(chunk, str):
            print(f"Received: {chunk}")
        else:
            print(f"Received chunk type: {type(chunk)}, value: {chunk}")


if __name__ == "__main__":
    asyncio.run(main())
