from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node
from brd_gen_agent.utils.llm import deepseek_llm
from langchain_core.messages import HumanMessage, SystemMessage
@logged_node
def write_section_node(state: SRSState, config=None) -> SRSState:
    idx = state["current_section_idx"]
    titles = state["outline"]
    if idx >= len(titles):
        return state  # 全部完成

    current_title = titles[idx]
    # 构造提示：撰写此标题下的详细内容，并引用上下文
    prompt = f"""请撰写《需求规格说明书》的“{current_title}”部分。
- 必须基于业务文档上下文撰写，并可在内容中注明来源文件（如“根据《xxx会议纪要》...”）。
- 严格遵循模板要求，如果是功能点，应包含：界面、输入/输出、业务流程及业务规则、异常处理。
- 禁止省略或使用“此处不再展开”，要提供完整细节。
- 输出仅包含该小节的内容，不要输出其他标题。

业务上下文：
{state["context_text"]}

模板指导（该章节的原始模板描述）：
{state["template_content"]}
"""
    response = deepseek_llm.invoke([HumanMessage(content=prompt)])
    # 存储到字典
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