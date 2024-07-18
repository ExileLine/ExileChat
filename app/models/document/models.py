# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 15:09
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from tortoise import fields

from common.libs.base_model import CustomBaseModel


class Document(CustomBaseModel):
    """文档"""

    able_id = fields.BigIntField(null=True, description='能力ID')
    name = fields.CharField(max_length=255, null=True, description='名称')
    doc_suffix = fields.CharField(max_length=16, null=True, description='文档后缀')
    handle_status = fields.CharField(max_length=16, null=True, description='处理情况:ready;success;fail')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_document"
