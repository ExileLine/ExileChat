# -*- coding: utf-8 -*-
# @Time    : 2024/10/11 18:57
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_llm_engine.py
# @Software: PyCharm

import asyncio

from aigc.llm_engine.llm_engine import LLMEngine
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

    print(engine.client)


if __name__ == "__main__":
    asyncio.run(main())
