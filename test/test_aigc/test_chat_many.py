# -*- coding: utf-8 -*-
# @Time    : 2024/10/11 17:26
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_chat_only.py
# @Software: PyCharm


import asyncio

from aigc.llm_engine.llm_engine import LLMEngine
from aigc.llm_chat.llm_chat import AigcChat
from api_key import api_key, azure_endpoint


async def main():
    """main"""

    engine = LLMEngine(
        company='azure_open_ai',
        api_key=api_key,
        client_options={
            "api_version": "2024-02-01",
            "azure_endpoint": azure_endpoint
        }
    )

    aigc_chat = AigcChat(client=engine.client, model="gpt4o")
    response_generator = aigc_chat.chat_many(input="你是谁?")
    async for chunk in response_generator:
        if isinstance(chunk, str):
            print(chunk)
        else:
            print(type(chunk), chunk)


if __name__ == "__main__":
    asyncio.run(main())
