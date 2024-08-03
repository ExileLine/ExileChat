# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 15:39
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from tortoise import fields

from common.libs.base_model import CustomBaseModel


class LLMCategory(CustomBaseModel):
    """大型语言模型分类"""

    name = fields.CharField(max_length=255, null=True, description='分类名称')
    is_public = fields.SmallIntField(default=1, null=True, description='是否公开')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_llm_category"


class LLM(CustomBaseModel):
    """大型语言模型"""

    category_id = fields.BigIntField(null=True, description='分类ID')
    name = fields.CharField(max_length=255, null=True, description='模型名称')
    api_key = fields.CharField(max_length=255, null=True, description='模型api_key')
    options = fields.JSONField(null=True, description='扩展参数选项')
    is_public = fields.SmallIntField(default=1, null=True, description='是否公开')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_llm"