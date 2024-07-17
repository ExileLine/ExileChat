# -*- coding: utf-8 -*-
# @Time    : 2024/4/28 18:02
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : common_paginate_query.py
# @Software: PyCharm

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from common.libs.common_page import page_size, query_result


async def cpq(request_data: BaseModel, Model, model_pydantic: BaseModel = None, like_list: list = None,
              where_list: list = None, order_by_list: list = None) -> dict:
    """
    通用分页模糊查询
    :param request_data: 入参
    :param Model: 模型
    :param model_pydantic: 使用`model_pydantic`处理`Model`数据
    :param like_list: 迷糊查询字段
    :param where_list: 只需要传入字段的名称例如：["name", ...] 在逻辑中会通过`request_data`组装成`精确查询条件`
    :param order_by_list: 排序字段名称降序加"-"号, 升序["id", ...] 降序["-id", ...]
    """

    filter_conditions = {}  # 模糊查询条件
    where_dict = {}  # 精确查询条件

    for k, v in request_data.dict().items():
        if v is None or bool(v) is False:
            continue
        if k in like_list:
            filter_conditions[f"{k}__icontains"] = v
        if k in where_list:
            where_dict[k] = v

    print(filter_conditions)
    print(where_dict)

    filter_conditions.update(where_dict)

    if not order_by_list:
        order_by_list = []

    page = request_data.page
    now_page = page
    size = request_data.size
    page, size = await page_size(page, size)

    # 获取未分页之前的总数（带有查询条件）
    total_count = await Model.filter(**filter_conditions).count()

    # 分页查询（同样带有相同查询条件）
    model_list = await Model.filter(**filter_conditions).offset(page).limit(size).order_by(*order_by_list)

    # 将查询结果转换为 Pydantic 模型
    if model_pydantic:
        model_list = [await model_pydantic.from_tortoise_orm(model) for model in model_list]

    # 将总数和分页后的结果一起传递给 query_result 函数
    data = await query_result(records=jsonable_encoder(model_list), now_page=now_page, total=total_count)
    return data
