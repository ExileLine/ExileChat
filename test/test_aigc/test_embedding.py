# -*- coding: utf-8 -*-
# @Time    : 2024/10/11 17:42
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_embedding.py
# @Software: PyCharm

import asyncio
from aigc.llm_engine.llm_engine import LLMEngine
from aigc.llm_embedding.llm_embedding import AigcEmbedding
from api_key import api_key


async def main():
    """main"""

    engine = LLMEngine(
        company='azure_open_ai',
        api_key=api_key,
        client_options={
            "api_version": "2024-02-01",
            "azure_endpoint": "https://by-openai.openai.azure.com/"
        }
    )

    aigc_embedding = AigcEmbedding(client=engine.client, model="embedding002", is_debug=True)
    result = await aigc_embedding.embedding("如何执行测试用例？")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
