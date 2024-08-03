# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 15:09
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from tortoise import fields

from common.libs.base_model import CustomBaseModel


class SecretaryCategory(CustomBaseModel):
    """助理分类"""

    name = fields.CharField(max_length=255, null=True, description='分类名称')
    is_public = fields.SmallIntField(default=1, null=True, description='是否公开')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_secretary_category"


class Secretary(CustomBaseModel):
    """助理"""

    category_id = fields.BigIntField(null=True, description='分类ID')
    cover = fields.CharField(max_length=1024, null=True, description='封面')
    name = fields.CharField(max_length=255, null=True, description='名称')
    introduce = fields.CharField(max_length=255, null=True, description='介绍')
    definition = fields.TextField(null=True, description='定义-prompt')
    llm_id = fields.BigIntField(null=True, description='大模型ID')
    llm_option = fields.JSONField(null=True, description='大模型-模型选项')
    plugins_option = fields.JSONField(null=True, description='插件选项')
    quick_question = fields.JSONField(null=True, description='快捷提问列表')
    answer_mode = fields.CharField(max_length=128, null=True, description='应答模式:free;stint;compatible')
    able_list = fields.JSONField(null=True, description='能力ID列表')
    is_public = fields.SmallIntField(default=1, null=True, description='是否公开')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_secretary"
