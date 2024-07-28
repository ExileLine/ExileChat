# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:56
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_document_vector.py
# @Software: PyCharm

import json
import asyncio

from api_key import api_key
from utils.ai.llm_engine import LLMEngine
from utils.ai.document_chunk import DocumentChunk
from utils.ai.document_vector import DocumentVector

if __name__ == '__main__':
    file_path = "/Users/yangyuexiong/Desktop/ExileChat/test/基于Python+Vue自动化测试平台的设计与实现.docx"
    dc = DocumentChunk(image_base_path="/Users/yangyuexiong/Desktop/ExileChat/test/test_ai", is_debug=True)
    document_content = dc.read_docx(file_path)
    # document_content = "1+1=2"
    new_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key)
    prompt = """你是一名文档解析专家，具备卓越的文档理解能力。你能够结合文档中的文字内容、图片和表格的上下文，准确地整理出详细的问答对话。请将这些结果以JSON字符串的形式输出，格式为：'[{"Q": "问题", "A": "答案"}...]'，请使用单引号来处理这个结果。
    以下是一个正确的例子
    [{"Q": "...","A": "..."}]
    以下是一个错误的例子
    ```json
    [{"Q": "...","A": "..."}]
    ```
    """
    dv = DocumentVector(document_content=document_content, llm_engine=new_engine, prompt=prompt)
    result = asyncio.run(dv.main())
    print(type(result), result)
    print(json.loads(result))
