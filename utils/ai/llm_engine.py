# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 17:32
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : llm_engine.py
# @Software: PyCharm

from types import MethodType, FunctionType

from openai import OpenAI, AzureOpenAI


class ModelClient:
    """Models Client"""

    api_key: str = None
    kwargs: dict = {}

    @classmethod
    def open_ai(cls):
        """OpenAI Client"""

        client = OpenAI(api_key=cls.api_key)
        return client

    @classmethod
    def azure_open_ai(cls):
        """AzureOpenAI Client"""

        api_version = cls.kwargs.get("api_version", "2024-02-01")
        azure_endpoint = cls.kwargs.get("azure_endpoint", "https://by-openai.openai.azure.com/")
        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=azure_endpoint,
            api_key=cls.api_key
        )
        return client

    @classmethod
    def moonshot(cls):
        """Moonshot Client"""

        base_url = cls.kwargs.get("base_url", "https://api.moonshot.cn/v1")
        client = OpenAI(
            api_key=cls.api_key,
            base_url=base_url,
        )
        return client


class LLMEngine:
    """Large Language Models Engine"""

    def __init__(self, model_name: str = None, api_key: str = None, is_debug: bool = False, *args, **kwargs):
        self.model_name = model_name
        self.api_key = api_key
        self.is_debug = is_debug
        self.args = args
        self.kwargs = kwargs

        ModelClient.api_key = api_key
        ModelClient.kwargs = kwargs
        self.client_dict = {
            "open_ai": ModelClient.open_ai,
            "azure_open_ai": ModelClient.azure_open_ai,
            "moonshot": ModelClient.moonshot,
        }
        self.client = self.client_init()

        self.system_prompt = "你是人工智能助手，你会为用户提供安全，有帮助，准确的回答。"
        self.system_messages = [{"role": "system", "content": self.system_prompt}]
        self.messages = []
        self.messages_limit = 20

    def client_init(self):
        """Client Init"""

        func = self.client_dict.get(self.model_name)
        if isinstance(func, MethodType):
            return func()
        else:
            raise KeyError("model_name not in client_dict key")

    async def make_messages(self, input: str) -> list[dict]:
        """消息构建"""

        self.messages.append({
            "role": "user",
            "content": input,
        })
        if len(self.messages) > self.messages_limit:
            return self.system_messages + self.messages[-self.messages_limit:]
        else:
            return self.system_messages + self.messages

    async def chat_only(self, prompt: str, input: str):
        """一次对话"""

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input},
        ]
        completion = self.client.chat.completions.create(
            model="gpt4o",
            messages=messages,
        )
        if completion and completion.choices and len(completion.choices) > 0:
            print("API 调用成功")
            generated_message = completion.choices[0].message.content
            return generated_message
        else:
            print("API 调用失败")
            return False

    async def chat(self, input: str):
        """对话"""

        await self.make_messages(input=input)

        completion = self.client.chat.completions.create(
            model="gpt4o",
            messages=self.messages,
            stream=True
        )

        current_content = ""
        for chunk in completion:
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                choice = chunk.choices[0]
                if choice.delta and hasattr(choice.delta, 'content'):
                    yield_content = choice.delta.content
                    if isinstance(yield_content, str):
                        current_content += yield_content
                    yield yield_content

        self.messages.append({
            "role": "user",
            "content": current_content,
        })

    async def embedding(self, text, *args, **kwargs):
        """向量"""

        response = self.client.embeddings.create(
            model="embedding002",
            input=text
        )
        if self.is_debug:
            print(response.data[0].embedding)
        return response.data[0].embedding

        # if self.model_name in ():
        #     pass
        # else:
        #     response = self.client.embeddings.create(
        #         model="embedding002",
        #         input=text
        #     )
        # print(response)
        # return response.data[0].embedding
