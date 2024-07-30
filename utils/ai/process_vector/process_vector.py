# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 19:04
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : process_vector.py
# @Software: PyCharm

from app.models.qa.models import QA
from app.models.document.models import Document
from utils.ai.prompt.qa_prompt import prompt
from utils.ai.llm_engine import LLMEngine
from utils.ai.document_chunk import DocumentChunk
from utils.ai.document_vector import DocumentVector


class ProcessVector:

    def __init__(self, document: Document, llm_engine: LLMEngine):
        """

        :param document: 文档模型对象 例如 `document = await Document.get_or_none(id=document_id)`
        :param llm_engine: 大模型引擎实例 例如 `llm_engine = LLMEngine(model_name='azure_open_ai', api_key=api_key)`
        """
        self.document = document
        self.llm_engine = llm_engine
        self.document_content = None  # 处理完毕的文档字符串
        self.vectored_qa_chunks = None  # 处理完毕的文档QA向量对象 -> list[dicy]

    async def call_dc(self):
        """调用`DocumentChunk`生成文档字符串"""

        dc = DocumentChunk(image_base_path="/Users/yangyuexiong/Desktop/ExileChat/test/test_ai", is_debug=True)
        self.document_content = dc.process_file(file_path=self.document.doc_path, file_ext=self.document.doc_suffix)
        return self.document_content

    async def call_dv(self):
        """调用`DocumentVector`生成文档向量"""

        dv = DocumentVector(document_content=self.document_content, llm_engine=self.llm_engine, prompt=prompt)
        qa_chunks = await dv.gen_qa_chunks()
        self.vectored_qa_chunks = await dv.gen_vector_qa_chunks(chunks=qa_chunks)
        return self.vectored_qa_chunks

    async def save_qa(self):
        """文档向量写入数据库"""

        if self.vectored_qa_chunks and isinstance(self.vectored_qa_chunks, list):
            for index, qa in enumerate(self.vectored_qa_chunks):
                remark = f"遍历索引_{index}"
                qa["remark"] = remark
                print(remark)
                await QA.create(**qa)

    async def main(self):
        """main"""

        try:
            self.document.handle_status = "ready"
            await self.document.save()
            await self.call_dc()
            await self.call_dv()
            await self.save_qa()
            self.document.handle_status = "success"
            await self.document.save()
        except BaseException as e:
            self.document.handle_status = "fail"
            self.document.remark = f"{e}"
            await self.document.save()
