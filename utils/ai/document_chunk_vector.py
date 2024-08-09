# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:09
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : document_chunk_vector.py
# @Software: PyCharm

import json

from utils.ai.llm_engine import LLMEngine
from utils.ai.prompt.chunks_prompt import chunks_prompt, replenish_prompt
from utils.ai.prompt.qa_prompt import qa_prompt
from app.models.chunk.models import Chunk
from app.models.qa.models import QA


class DocumentChunkVector:
    """
    文档向量
    1.接收已经处理好的文档字符串
    2.接收大模型引擎`LLMEngine`实例
    3.使用`LLMEngine`结合`prompt`文档生成`chunks`
    4.使用`LLMEngine`结合`prompt`对段落生成`QA`
    5.生成`QA`向量写入数据库
    """

    def __init__(self, document_content: str, llm_engine: LLMEngine, prompt: str = None, is_debug: bool = False,
                 db_init: bool = False):
        """

        :param document_content: 文档字符串
        :param llm_engine: 大模型引擎实例
        :param prompt: 生成`chunks`提示词, 默认使用: chunks_prompt()
        :param is_debug: 提示模式, 输出`print`
        """
        self.document_content = document_content
        self.document_content_length = len(document_content)
        self.llm_engine = llm_engine
        if prompt:
            self.prompt = prompt
        else:
            self.prompt = chunks_prompt(original=self.document_content)
        self.is_debug = is_debug
        self.db_init = db_init

        self.gen_chunks_sw = True
        self.gen_chunks_rounds = 1
        self.chunks_length = 0
        self.chunks = []
        self.qa = []
        self.qa_loads_fail = []
        self.qa_vector = []

    async def handle_chunks_str(self, response_chunks: str):
        """处理提取段落"""

        for index, chunk in enumerate(response_chunks.split("<chunks>")):

            strip_chunk = chunk.strip()

            if "</chunks>" in strip_chunk:  # 完整的段落
                content = strip_chunk.replace("</chunks>", "")
                data = {
                    "index": index,
                    "content": content
                }
                self.chunks.append(data)
                self.chunks_length += len(content)
                self.gen_chunks_sw = False
                if self.is_debug:
                    print(f"分段完成x: === {strip_chunk} ===")

            else:  # 不完整的段落(会因为篇幅太长导致大模型无法相应完整的应答,记录中断之前的段落,再次结合原文补充生成)
                self.gen_chunks_sw = True

        if "<success>分段完成</success>" in response_chunks:
            self.gen_chunks_sw = False
            if self.is_debug:
                print(f"分段完成y: === {response_chunks} ===")

    async def gen_chunks(self):
        """生成`chunks`对象"""

        print("=== gen_chunks ===")

        while self.gen_chunks_sw:
            print("=== gen_chunks_rounds ===", self.gen_chunks_rounds)
            if self.gen_chunks_rounds == 1:
                response_chunks = await self.llm_engine.chat_only(
                    prompt=self.prompt,
                    input="根据原文分段"
                )
            else:
                if not self.chunks:
                    raise ValueError("属性 success_chunks 异常")

                content = self.chunks[-1].get("content")
                if self.is_debug:
                    print(f"=== 中断段落 ===\n{content}")
                current_prompt = replenish_prompt(original=self.document_content, node=content)
                response_chunks = await self.llm_engine.chat_only(
                    prompt=current_prompt,
                    input="根据原文从标签<before>分段"
                )

            if self.is_debug:
                print(response_chunks)

            await self.handle_chunks_str(response_chunks=response_chunks)
            self.gen_chunks_rounds += 1

            if self.is_debug:
                print(f"原文长度: {self.document_content_length}")
                print(f"段落累计长度: {self.chunks_length}")

            # 原文长度大于段落总长度，继续执行(不严谨的逻辑)。
            # if self.document_content_length > self.chunks_length:
            #     self.gen_chunks_sw = True

        await self.get_json_chunks()

        return self.chunks

    async def save_chunks(self):
        """持久化保存`chunks`在数据库中"""

        for data in self.chunks:
            chunk = Chunk(**data)
            await chunk.save()

    async def get_json_chunks(self):
        """后去json格式的`chunks`"""

        json_chunks = json.dumps(self.chunks, ensure_ascii=False)
        if self.is_debug:
            print(json_chunks)
        return json_chunks

    async def gen_qa(self):
        """生成`QA`"""

        print("=== gen_qa ===")

        current_prompt = qa_prompt

        if self.chunks:
            for index, sc in enumerate(self.chunks):
                chunk = sc.get("content")
                if self.is_debug:
                    print(index, chunk)
                qa_list_str = await self.llm_engine.chat_only(prompt=current_prompt, input=chunk)
                if qa_list_str:
                    try:
                        qa_list = json.loads(qa_list_str)
                        self.qa += qa_list
                    except BaseException as e:
                        self.qa_loads_fail.append(qa_list_str)  # TODO 处理序列化失败的数据

        if self.is_debug:
            print(self.qa)

        return self.qa

    async def gen_qa_vector(self):
        """生成`QA`向量"""

        print("=== gen_qa_vector ===")

        if self.qa:
            for qa in self.qa:
                question = qa.get("Q")
                answer = qa.get("A")
                chunks = qa.get("chunks")
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
                self.qa_vector.append(data)

        if self.is_debug:
            print(self.qa_vector)

        return self.qa_vector

    async def save_qa(self):
        """持久化保存`QA`在数据库中"""

        for data in self.qa_vector:
            qa = QA(**data)
            await qa.save()

    async def test(self):
        """test"""

        if self.db_init:
            from utils.db_connect import db_init_pg
            await db_init_pg()

        await self.gen_chunks()
        await self.save_chunks()
        await self.gen_qa()
        await self.gen_qa_vector()
        await self.save_qa()
