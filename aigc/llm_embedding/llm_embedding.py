# -*- coding: utf-8 -*-
# @Time    : 2024/10/11 17:39
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : llm_embedding.py
# @Software: PyCharm


class AigcEmbedding:
    """向量"""

    def __init__(self, client, model, is_debug=False):
        """

        :param client:
        :param model: embedding002...
        :param is_debug:
        """
        self.client = client
        self.model = model
        self.is_debug = is_debug

    async def embedding(self, text, *args, **kwargs):
        """向量"""

        response = self.client.embeddings.create(
            model=self.model,
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
