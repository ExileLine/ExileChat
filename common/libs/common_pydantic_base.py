# -*- coding: utf-8 -*-
# @Time    : 2024/5/10 14:34
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : common_pydantic_base.py
# @Software: PyCharm


from pydantic import BaseModel
from typing import Union

"""
exclude_unset：是否排除未明确设置的字段。 
exclude_defaults：是否排除设置为默认值的字段。 
exclude_none：是否排除值为“None”的字段。
"""


class CommonPydanticCreate(BaseModel):
    remark: str = "新增"
    creator: str = "test_creator"
    creator_id: int = 0

    def dict(self, **kwargs):
        """重写 dict() 方法，在每次调用时带上指定参数: exclude_unset=True"""
        return super().dict(exclude_unset=True, **kwargs)


class CommonPydanticUpdate(BaseModel):
    id: Union[int, None] = None
    remark: str = "编辑"
    modifier: str = "test_modifier"
    modifier_id: int = 0

    def dict(self, **kwargs):
        """重写 dict() 方法，在每次调用时带上指定参数: exclude_unset=True, exclude_defaults=True, exclude_none=True"""
        return super().dict(exclude_unset=True, exclude_defaults=True, exclude_none=True, **kwargs)
