# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 19:04
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : process_vector.py
# @Software: PyCharm

from app.models.document.models import Document
from aigc.llm_chat.llm_chat import AigcChat
from aigc.llm_embedding.llm_embedding import AigcEmbedding
from aigc.rag.document_parser import DocumentParser
from aigc.rag.document_chunk_vector import DocumentChunkVector


class ProcessVector:

    def __init__(self, document: Document, aigc_chat: AigcChat, aigc_embedding: AigcEmbedding, is_debug: bool = False):
        """

        :param document: 文档模型对象 例如 `document = await Document.get_or_none(id=document_id)`
        """
        self.document = document
        self.aigc_chat = aigc_chat
        self.aigc_embedding = aigc_embedding
        self.is_debug = is_debug
        self.document_content = None  # 处理完毕的文档字符串
        self.vectored_qa_chunks = None  # 处理完毕的文档QA向量对象 -> list[dicy]

    async def call_document_parser(self):
        """调用`DocumentParser`生成文档字符串"""

        dc = DocumentParser(
            image_base_path="/test/test_aigc",
            is_debug=self.is_debug
        )
        self.document_content = dc.process_file(file_path=self.document.doc_path, file_ext=self.document.doc_suffix)
        return self.document_content

    async def call_document_chunk_vector(self):
        """调用`DocumentChunkVector`生成文档向量"""

        dv = DocumentChunkVector(
            document_content=self.document_content,
            llm_chat=self.aigc_chat,
            llm_embedding=self.aigc_embedding,
            is_debug=self.is_debug
        )
        await dv.gen_chunks()
        await dv.save_chunks()
        await dv.gen_qa()
        await dv.gen_qa_vector()
        await dv.save_qa()

    async def main(self):
        """main"""

        try:
            self.document.handle_status = "ready"
            await self.document.save()

            await self.call_document_parser()
            await self.call_document_chunk_vector()

            self.document.handle_status = "success"
            await self.document.save()
        except BaseException as e:
            self.document.handle_status = "fail"
            self.document.remark = f"{e}"
            await self.document.save()
