# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:09
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : document_vector.py
# @Software: PyCharm

import json

from utils.ai.llm_engine import LLMEngine


class DocumentVector:
    """
    文档向量
    1.接收已经处理好的文档字符串
    2.接收大模型引擎`LLMEngine`实例
    3.使用`LLMEngine`结合`prompt`分成对应`QA chunks`
    4.把这些`QA chunks`向量写入数据库
    """

    def __init__(self, document_content: str, llm_engine: LLMEngine, prompt: str, is_debug: bool = False):
        self.document_content = document_content
        self.llm_engine = llm_engine
        self.prompt = prompt
        self.is_debug = is_debug

    async def gen_qa_chunks(self):
        """生成`QA chunks`"""

        qa_chunks_str = await self.llm_engine.chat_only(prompt=self.prompt, input=self.document_content)
        if self.is_debug:
            print(type(qa_chunks_str), qa_chunks_str)
        if qa_chunks_str:
            try:
                qa_chunks_json = json.loads(qa_chunks_str)
                return qa_chunks_json
            except BaseException as e:
                raise TypeError(f"qa_chunks JSON序列化失败：{e}")
        else:
            raise TypeError(f"生成 qa_chunks_str 出现异常")

    async def gen_vector_qa_chunks(self, chunks: list[dict]) -> list[dict]:
        """生成`QA chunks`向量"""

        vectored_qa_chunks = []

        for chunk in chunks:
            question = chunk.get("Q")
            answer = chunk.get("A")
            chunks = chunk.get("chunks")
            question_embedding = await self.llm_engine.embedding(text=question)
            answer_embedding = await self.llm_engine.embedding(text=answer)

            data = {
                "able_id": 0,
                "document_id": 0,
                "answer": answer,
                "question": question,
                "chunks": chunks,
                "question_embedding": json.dumps(question_embedding, ensure_ascii=False),
                "answer_embedding": json.dumps(answer_embedding, ensure_ascii=False)
            }
            vectored_qa_chunks.append(data)

        return vectored_qa_chunks
