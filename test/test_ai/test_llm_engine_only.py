# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:28
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_llm_engine_only.py
# @Software: PyCharm

import asyncio
from utils.ai.llm_engine import LLMEngine
from api_key import api_key


async def main():
    """main"""

    new_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key)
    generated_message = await new_engine.chat_only(prompt="你是强大的人工智能", input="你是谁?")
    print(generated_message)


if __name__ == "__main__":
    asyncio.run(main())
