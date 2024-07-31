# -*- coding: utf-8 -*-
# @Time    : 2024/7/31 13:40
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : chunks_prompt.py
# @Software: PyCharm

chunks_prompt = """
你是一名文档解析专家，具备卓越的文档理解能力。你的任务是根据理解上下文，将文档内容结合上下文分段。
注意事项：请保持原文内容一字不漏合理分段，并将合理分段的内容按以下格式输出
<chunks>
合理分段1
</chunks>
<chunks>
合理分段2
</chunks>
<chunks>
合理分段3
</chunks>
"""


def replenish_prompt(content: str):
    """replenish_prompt"""

    func_prompt = f"""你是一名文档解析专家，具备卓越的文档理解能力。你的任务是根据文档的上下文，将内容准确划分为段落。从我提供的部分之后开始，不要包括我提供的这部分内容。我提供的部分在标签 <before>...</before> 中。
<before>
{content}
</before>
注意事项：请保持原文内容一字不漏合理分段，并将合理分段的内容按以下格式输出
<chunks>
合理分段1
</chunks>
<chunks>
合理分段2
</chunks>
<chunks>
合理分段3
</chunks>
    """

    return func_prompt
