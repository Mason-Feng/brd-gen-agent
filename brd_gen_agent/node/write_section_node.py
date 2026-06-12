from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node
from brd_gen_agent.utils.llm import deepseek_llm
from langchain_core.messages import HumanMessage

from typing import List, Dict


def get_section_instruction(title: str, template_sections: List[Dict[str, str]]) -> str:
    normalized = title.strip()
    for section in template_sections:
        if section.get("heading", "").strip() == normalized:
            return section.get("instruction", "")
    # fallback: compare bare title text without hashes
    bare_title = normalized.lstrip('#').strip()
    for section in template_sections:
        if section.get("title", "").strip() == bare_title:
            return section.get("instruction", "")
    return ""


@logged_node
def write_section_node(state: SRSState, config=None) -> SRSState:
    idx = state["current_section_idx"]
    titles = state["outline"]
    if idx >= len(titles):
        return state  # 全部完成

    current_title = titles[idx]
    template_sections = state.get("template_sections", [])
    section_instruction = get_section_instruction(current_title, template_sections)

    prompt = f"""请撰写《需求规格说明书》的“{current_title}”部分。
- 必须基于业务文档上下文撰写。
- 严格遵循该章节的模板填写要求：
{section_instruction if section_instruction else '（模板中未提供该章节的具体填写要求）'}
- 如果是功能需求，应包含：界面、输入/输出、业务流程及业务规则、异常处理。
- 禁止省略或使用“此处不再展开”，要提供完整细节。
- 输出仅包含该小节的内容，不要输出其他标题。

业务上下文：
{state["context_text"]}
"""
    response = deepseek_llm.invoke([HumanMessage(content=prompt)])
    new_sections = dict(state["sections_content"])
    new_sections[current_title] = response.content
    new_idx = idx + 1
    return {"sections_content": new_sections, "current_section_idx": new_idx}

# 条件边函数
def should_continue_sections(state: SRSState) -> str:
    if state["current_section_idx"] < len(state["outline"]):
        return "write_section"
    else:
        return "assemble_document"