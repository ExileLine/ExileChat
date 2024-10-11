# -*- coding: utf-8 -*-
# @Time    : 2024/8/13 14:49
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : llm_engine.py
# @Software: PyCharm

from openai import OpenAI
from openai.lib.azure import AzureOpenAI


class ModelClient:
    """Models Client"""

    def __init__(self, api_key: str = None, client_options: dict = None):
        self.api_key = api_key
        self.client_options = client_options

    def open_ai(self):
        """OpenAI Client"""

        client = OpenAI(api_key=self.api_key)
        return client

    def azure_open_ai(self):
        """AzureOpenAI Client"""

        api_version = self.client_options.get("api_version")
        azure_endpoint = self.client_options.get("azure_endpoint")
        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=azure_endpoint,
            api_key=self.api_key
        )
        return client

    def moonshot(self):
        """Moonshot Client"""

        base_url = self.client_options.get("base_url", "https://api.moonshot.cn/v1")
        client = OpenAI(
            api_key=self.api_key,
            base_url=base_url,
        )
        return client


class LLMEngine:
    """Large Language Models Engine"""

    default_system_prompt = "你是人工智能助手，你会为用户提供安全，有帮助，准确的回答。"

    def __init__(self, company: str = None, api_key: str = None, client_options: dict = None):
        """

        :param company: open_ai、azure_open_ai、moonshot、...
        :param api_key: 大模型`ApiKey`
        :param client_options: 例如 {"api_version": "2024-02-01", "azure_endpoint": "https://xxx.openai.azure.com/",...}
        """

        self.company = company
        self.api_key = api_key
        self.client_options = client_options if client_options else {}

        if not hasattr(ModelClient, self.company):
            raise AttributeError(f"The model client does not have the attribute '{self.company}'!!!")

        self.model_client = ModelClient(api_key=self.api_key, client_options=self.client_options)
        self.client = getattr(self.model_client, self.company)()
