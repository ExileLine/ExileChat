# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 15:09
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from tortoise import fields

from common.libs.base_model import CustomBaseModel


class Chat(CustomBaseModel):
    """对话"""

    name = fields.CharField(max_length=255, null=True, description='对话名称')
    option_json = fields.JSONField(null=True, description='对话选项对象')
    chat_type = fields.CharField(max_length=32, null=True, description='对话类型:normal;able')
    secretary_id = fields.BigIntField(null=True, description='助手ID')
    able_id = fields.BigIntField(null=True, description='能力ID')
    prompt = fields.TextField(null=True, description='提示词')
    use_prompt = fields.SmallIntField(null=True, default=0, description='是否使用自定义提示词')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_chat"


class ChatHistory(CustomBaseModel):
    """对话历史"""

    chat_id = fields.BigIntField(null=True, description='对话ID')
    role = fields.CharField(max_length=128, null=True, description='角色')
    content = fields.TextField(null=True, description='内容')
    tokens = fields.BigIntField(null=True, description='消耗')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_chat_history"


class ChatAnswerTrack(CustomBaseModel):
    """对话应答监测"""

    chat_id = fields.BigIntField(null=True, description='对话ID')
    node_link = fields.JSONField(null=True, description='节点链路:chat_history_id_list')
    target_node_id = fields.BigIntField(null=True, description='作用节点:chat_history_id')
    user_action = fields.CharField(max_length=128, null=True, description='用户动作:copy;reload;share;like;dislike')
    creator = fields.CharField(max_length=32, null=True, description="创建人")
    creator_id = fields.BigIntField(null=True, description="创建人id")
    modifier = fields.CharField(max_length=32, null=True, description='更新人')
    modifier_id = fields.BigIntField(null=True, description='更新人id')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        table = "ec_chat_answer_track"
