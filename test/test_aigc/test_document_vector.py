# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:56
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_document_vector.py
# @Software: PyCharm

import asyncio

from api_key import api_key, azure_endpoint
from aigc.llm_engine.llm_engine import LLMEngine
from aigc.llm_chat.llm_chat import AigcChat
from aigc.llm_embedding.llm_embedding import AigcEmbedding

from aigc.rag.document_parser import DocumentParser
from aigc.rag.document_chunk_vector import DocumentChunkVector
from utils.db_connect import db_init_pg
from app.models.chunk.models import Chunk


async def save_db(save_data: list):
    """写入数据库"""

    await db_init_pg()
    for data in save_data:
        chunk = Chunk(**data)
        await chunk.save()


if __name__ == '__main__':
    is_debug = True
    # file_path = "/Users/yangyuexiong/Desktop/ExileChat/test/基于Python+Vue自动化测试平台的设计与实现.docx"
    file_path = "/test/测试文档分段.docx"
    dc = DocumentParser(image_base_path="/test/test_ai", is_debug=is_debug)
    document_content = dc.process_file(file_path)

    # document_content = "1+1=2"

    engine = LLMEngine(
        company='azure_open_ai',
        api_key=api_key,
        client_options={
            "api_version": "2024-02-01",
            "azure_endpoint": azure_endpoint
        }
    )
    aigc_chat = AigcChat(client=engine.client, model="gpt4o")
    aigc_embedding = AigcEmbedding(client=engine.client, model="embedding002", is_debug=True)
    dv = DocumentChunkVector(
        document_content=document_content,
        llm_chat=aigc_chat,
        llm_embedding=aigc_embedding,
        is_debug=is_debug,
        db_init=True
    )
    asyncio.run(dv.test())

    # asyncio.run(dv.gen_chunks())
    # asyncio.run(dv.save_chunks())
    # asyncio.run(dv.gen_qa())
    # asyncio.run(dv.gen_qa_vector())
    # asyncio.run(dv.save_qa())

    # print("=== qa_vector ===")
    # asyncio.run(save_db(save_data=success_chunks))
