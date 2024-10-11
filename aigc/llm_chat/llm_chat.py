# -*- coding: utf-8 -*-
# @Time    : 2024/10/11 17:28
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : llm_chat.py
# @Software: PyCharm


class AigcChat:
    """对话"""

    default_system_prompt = "你是人工智能助手，你会为用户提供安全，有帮助，准确的回答。"

    def __init__(self, client, model, system_prompt=None):
        """
        :param client:
        :param model: gpt4o、gpt4、gpt3.5、...
        :param system_prompt:
        """
        self.client = client
        self.model = model
        self.system_prompt = system_prompt if system_prompt else self.default_system_prompt
        self.system_messages = [{"role": "system", "content": self.system_prompt}]
        self.messages = []
        self.messages_limit = 20

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
            model=self.model,
            messages=messages,
        )
        if completion and completion.choices and len(completion.choices) > 0:
            print("API 调用成功")
            generated_message = completion.choices[0].message.content
            return generated_message
        else:
            print("API 调用失败")
            return False

    async def chat_many(self, input: str):
        """多轮对话"""

        await self.make_messages(input=input)

        completion = self.client.chat.completions.create(
            model=self.model,
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
            "role": "assistant",
            "content": current_content,
        })
