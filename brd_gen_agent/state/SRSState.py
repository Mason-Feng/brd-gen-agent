from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END

class SRSState(TypedDict):
    # 输入参数
    folder_path: str                # 业务文档所在文件夹路径
    codebase_path: Optional[str]    # 代码库路径，若无可为 None
    template_path: str              # 业务需求规格说明书模板路径
    project_name: str               # 输出文件名，可从模板或用户获取

    # 中间过程
    documents: List[Dict[str, str]] # {"path": "相对路径", "content": "文本内容"}
    context_text: str               # 拼接后的全文上下文
    template_content: str           # 模板原文
    outline: List[str]              # 大纲标题列表，如 ["## 1. 引言", "## 2. 总体描述", ...]
    sections_content: Dict[str, str] # key: 标题, value: 生成的内容
    current_section_idx: int        # 当前撰写章节索引

    # 结果
    final_srs: str                  # 生成的业务需求规格说明书文本
    status: str                     # "running", "completed", "error"
    error_message: str              # 错误信息，若无错误则为空字符串