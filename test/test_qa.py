# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 20:54
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_qa.py
# @Software: PyCharm


import json
from tortoise import run_async

from utils.db_connect import db_init_pg
from app.models.qa.models import QA

answer_embedding = [0.02715362422168255, -0.010939446277916431, 0.006153851747512817, -0.009505090303719044]
question_embedding = [0.02715362422168255, -0.010939446277916431, 0.006153851747512817, -0.009505090303719044]


async def main():
    """main"""

    await db_init_pg()
    qa = {
        'able_id': 0,
        'document_id': 0,
        'answer': '1+1等于2',
        'question': '1+1等于几？',
        'chunks': ["原文段落1", "原文段落2"],
        'answer_embedding': json.dumps(answer_embedding, ensure_ascii=False),
        'question_embedding': json.dumps(question_embedding, ensure_ascii=False),
    }
    await QA.create(**qa)


if __name__ == '__main__':
    run_async(main())
