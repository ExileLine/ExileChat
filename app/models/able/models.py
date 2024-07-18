# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 15:09
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from tortoise import fields

from common.libs.base_model import CustomBaseModel


class Able(CustomBaseModel):
    """能力"""

    able_category_id = fields.BigIntField(null=True, description='分类ID')
    cover = fields.CharField(max_length=1024, null=True, description='封面')
    name = fields.CharField(max_length=255, null=True, description='名称')
    introduce = fields.CharField(max_length=255, null=True, description='介绍')
    vector_llm_id = fields.BigIntField(null=True, description='向量大模型ID')
    is_public = fields.SmallIntField(default=1, null=True, description='是否公开')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_able"
