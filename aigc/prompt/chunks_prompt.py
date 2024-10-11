# -*- coding: utf-8 -*-
# @Time    : 2024/7/31 13:40
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : chunks_prompt.py
# @Software: PyCharm

def chunks_prompt(original: str):
    """chunks prompt"""

    chunks_prompt = f"""你是一名文档解析专家，具备卓越的文档理解能力。你的任务是根据标签 <original>...</original> 内的原文文档内容，理解上下文并将其准确划分为段落。
<original>
{original}
</original>
以下是对你的具体要求：
1.保持段落的原始顺序。
2.确保每个段落保持原文内容，合理分段，并按以下标签 <chunks>...</chunks> 格式将段落输出。
3.全文分段完毕后，在末尾增加标签 <success>分段完成</success> 。 

例子：
<chunks>
合理分段1
</chunks>
<chunks>
合理分段2
</chunks>
<chunks>
合理分段3
</chunks>
<success>分段完成</success>
"""
    return chunks_prompt


def replenish_prompt(original: str, node: str):
    """replenish prompt"""

    func_prompt = f"""你是一名文档解析专家，具备卓越的文档理解能力。
你的任务是根据标签 <original>...</original> 内的原文文档内容中找出标签 <before>...</before> 提供内容的结尾处开始解析，将其准确划分为段落，直到原文文档内容结束。
将其准确划分为段落。请从标签 <before>...</before> 提供内容的结尾处开始解析，忽略标签内的内容，直到原文文档内容结束。
<original>
{original}
</original>    
<before>
{node}
</before>
以下是对你的具体要求：
1.划分段落时，不包括标签 <before> 内的内容。
2.保持段落的原始顺序。
3.在解析原文文档内容结束后，不要重新开始。
4.确保每个段落保持原文内容，合理分段，并按以下标签 <chunks>...</chunks> 格式将段落输出。
5.全文分段完毕后，在末尾增加标签 <success>分段完成</success> 。 

例子：
<chunks>
合理分段1
</chunks>
<chunks>
合理分段2
</chunks>
<chunks>
合理分段3
</chunks>
<success>分段完成</success>
"""

    return func_prompt
