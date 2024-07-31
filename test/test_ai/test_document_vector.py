# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:56
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_document_vector.py
# @Software: PyCharm

import asyncio

from api_key import api_key
from utils.ai.llm_engine import LLMEngine
from utils.ai.document_chunk import DocumentChunk
from utils.ai.document_vector import DocumentVector

if __name__ == '__main__':
    is_debug = True
    # file_path = "/Users/yangyuexiong/Desktop/ExileChat/test/基于Python+Vue自动化测试平台的设计与实现.docx"
    file_path = "/Users/yangyuexiong/Desktop/ExileChat/test/测试文档分段.docx"
    dc = DocumentChunk(image_base_path="/Users/yangyuexiong/Desktop/ExileChat/test/test_ai", is_debug=is_debug)
    document_content = dc.process_file(file_path)

    # document_content = "1+1=2"

    llm_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key, is_debug=is_debug)
    dv = DocumentVector(document_content=document_content, llm_engine=llm_engine, is_debug=is_debug)
    asyncio.run(dv.gen_chunks())
    asyncio.run(dv.gen_qa())
    asyncio.run(dv.gen_qa_vector())
