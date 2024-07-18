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

    -- 手动创建`ivfflat`索引
    CREATE INDEX ON ec_qa USING ivfflat (question_embedding) WITH (lists = 100);
    CREATE INDEX ON ec_qa USING ivfflat (answer_embedding) WITH (lists = 100);
    """

    question = fields.TextField(null=True, description='问题')
    answer = fields.TextField(null=True, description='答案')
    question_embedding = VectorField(null=True, description='问题向量')
    answer_embedding = VectorField(dimension=1600, null=True, description='答案向量')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_qa"
