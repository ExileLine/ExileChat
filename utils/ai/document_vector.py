# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 02:09
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : document_vector.py
# @Software: PyCharm

from utils.ai.llm_engine import LLMEngine


class DocumentVector:
    """
    文档向量
    1.接收已经处理好的文档字符串
    2.接收大模型引擎`LLMEngine`实例
    3.使用`LLMEngine`结合`prompt`分成对应`QA chunks`
    4.把这些`QA chunks`向量写入数据库
    """

    def __init__(self, document_content: str, llm_engine: LLMEngine, prompt: str):
        self.document_content = document_content
        self.llm_engine = llm_engine
        self.prompt = prompt

    async def main(self):
        """main"""

        result_content = await self.llm_engine.chat_only(prompt=self.prompt, input=self.document_content)
        return result_content