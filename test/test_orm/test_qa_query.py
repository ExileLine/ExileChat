# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 03:00
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_qa_query.py
# @Software: PyCharm

import json

from tortoise import Tortoise, run_async

from utils.db_connect import db_init_pg
from test.test_orm.data import v1

sql_demo = """
SELECT
	*,
	question_embedding <-> '[-0.0018926516640931368, -0.008093692362308502, 0.0063547855243086815]'::vector AS distance
FROM
	ec_qa
WHERE
	question_embedding <-> '[-0.0018926516640931368, -0.008093692362308502, 0.0063547855243086815]'::vector <= 0.50
ORDER BY
	distance ASC;
"""


async def qa_query(*args):
    """qa向量查询"""

    await db_init_pg()

    sql = """
    SELECT
	    id,
	    able_id,
	    document_id,
	    question,
	    answer,
        question_embedding <-> $1::vector AS distance
    FROM
        ec_qa
    WHERE
        question_embedding <-> $1::vector <= $2
    ORDER BY
        distance ASC;
    """
    print(sql)

    result = await Tortoise.get_connection('default').execute_query_dict(sql, args)
    print(result)
    return result


if __name__ == '__main__':
    vector = str(v1)
    distance_threshold = 0.50
    print(run_async(qa_query(vector, distance_threshold)))
