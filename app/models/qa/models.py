# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 15:09
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

import numpy as np
from tortoise import fields

from common.libs.base_model import CustomBaseModel


class VectorField(fields.Field):
    SQL_TYPE = "VECTOR"

    def __init__(self, dimension=None, *args, **kwargs):
        self.dimension = dimension
        super().__init__(*args, **kwargs)

    def to_db_value(self, value, instance):
        if isinstance(value, np.ndarray):
            return value.tolist()
        return value

    def to_python_value(self, value):
        if isinstance(value, list):
            return np.array(value)
        return value

    def to_schema(self):
        return f"VECTOR({self.dimension})" if self.dimension else "VECTOR"


class QA(CustomBaseModel):
    """问答

    安装`pgvector`扩展:
        CREATE EXTENSION IF NOT EXISTS vector;

    手动创建`ivfflat`索引(需要对应的字段指定了维度才能创建索引)

    指定维度:
        CREATE INDEX ON ec_qa USING ivfflat (question_embedding) WITH (lists = 1600);
        CREATE INDEX ON ec_qa USING ivfflat (answer_embedding) WITH (lists = 1600);

    创建索引:
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_question_embedding_ivfflat ON ec_qa
            USING ivfflat (question_embedding vector_l2_ops);

        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_answer_embedding_ivfflat ON ec_qa
            USING ivfflat (answer_embedding vector_l2_ops);
    """

    able_id = fields.BigIntField(null=True, description='能力ID')
    document_id = fields.BigIntField(null=True, description='文档ID')
    question = fields.TextField(null=True, description='问题')
    answer = fields.TextField(null=True, description='答案')
    question_embedding = VectorField(null=True, description='问题向量')
    answer_embedding = VectorField(dimension=1600, null=True, description='答案向量')
    like = fields.BigIntField(null=True, default=0, description='赞')
    dislike = fields.BigIntField(null=True, default=0, description='踩')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_qa"
