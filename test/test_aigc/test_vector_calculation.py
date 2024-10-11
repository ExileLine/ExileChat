# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 03:57
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_vector_calculation.py
# @Software: PyCharm

import numpy as np

# 定义两个向量
vector1 = np.array([0.2, 0.2, 0.8])
vector2 = np.array([0.2, 0.2, 0.1])


# vector2 = np.array([0.2, 0.2, 0.6]) # 0.9949366763261821
# vector2 = np.array([0.2, 0.2, 0.5]) # 0.9847319278346619
# vector2 = np.array([0.2, 0.2, 0.4]) # 0.9622504486493764
# vector2 = np.array([0.2, 0.2, 0.3]) # 0.914659120760047
# vector2 = np.array([0.2, 0.2, 0.2]) # 0.8164965809277259
# vector2 = np.array([0.2, 0.2, 0.1]) # 0.628539361054709


def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)


if __name__ == '__main__':
    # 计算余弦相似度
    similarity = cosine_similarity(vector1, vector2)
    print(f"Cosine Similarity: {similarity}")

    # 计算欧氏距离
    euclidean_distance = np.linalg.norm(vector1 - vector2)
    print(f"Euclidean Distance: {euclidean_distance}")
