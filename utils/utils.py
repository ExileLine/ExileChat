# -*- coding: utf-8 -*-
# @Time    : 2024/7/27 15:36
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : utils.py
# @Software: PyCharm

from dateutil import parser


def convert_to_standard_format(datetime_str: str) -> str:
    """
    时间格式化处理
    输出例如: `2024-07-27 15:22:31`
    """

    try:
        dt = parser.parse(datetime_str)  # 解析未知格式的日期时间字符串
        formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')  # 将日期时间对象格式化为指定的格式
        return formatted_dt
    except BaseException as e:  # 异常返回原数据
        return datetime_str


if __name__ == '__main__':
    print(convert_to_standard_format("2024-07-27 15:45:30.292836+08"))
    print(convert_to_standard_format("2024-07-27T15:45:30"))
    print(convert_to_standard_format("2024-07-27 09:39:53.000000"))
    print(convert_to_standard_format("test error"))
