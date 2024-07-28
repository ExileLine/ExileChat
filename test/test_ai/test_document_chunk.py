# -*- coding: utf-8 -*-
# @Time    : 2024/7/27 17:14
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_document_chunk.py
# @Software: PyCharm


from utils.ai.document_chunk import DocumentChunk

if __name__ == "__main__":
    file_path = "/Users/yangyuexiong/Desktop/ExileChat/test/测试文档.docx"
    dc = DocumentChunk(image_base_path="/Users/yangyuexiong/Desktop/ExileChat/test/test_ai", is_debug=True)
    dc.read_docx(file_path)
