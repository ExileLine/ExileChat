# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:56
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_document_vector.py
# @Software: PyCharm

import json
import asyncio

from api_key import api_key
from utils.ai.prompt.qa_prompt import prompt
from utils.ai.llm_engine import LLMEngine
from utils.ai.document_chunk import DocumentChunk
from utils.ai.document_vector import DocumentVector

if __name__ == '__main__':
    file_path = "/Users/yangyuexiong/Desktop/ExileChat/test/基于Python+Vue自动化测试平台的设计与实现.docx"
    dc = DocumentChunk(image_base_path="/Users/yangyuexiong/Desktop/ExileChat/test/test_ai", is_debug=True)
    document_content = dc.read_docx(file_path)
    # document_content = "1+1=2"
    new_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key)
    dv = DocumentVector(document_content=document_content, llm_engine=new_engine, prompt=prompt)
    qa_chunks_json = asyncio.run(dv.gen_qa_chunks())
    eb_result = asyncio.run(dv.gen_vector_qa_chunks(chunks=qa_chunks_json))
    print(json.dumps(qa_chunks_json, ensure_ascii=False))
