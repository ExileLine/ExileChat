# -*- coding: utf-8 -*-
# @Time    : 2024/7/31 17:10
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_process_file.py
# @Software: PyCharm

from aigc.rag.document_parser import DocumentParser

if __name__ == '__main__':
    is_debug = True
    file_path = "../test/测试文档分段.docx"
    dc = DocumentParser(image_base_path="/test/test_aigc", is_debug=is_debug)
    document_content = dc.process_file(file_path)
