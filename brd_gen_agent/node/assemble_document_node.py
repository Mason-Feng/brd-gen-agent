from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node
@logged_node
def assemble_document_node(state: SRSState, config=None) -> SRSState:
    parts = []
    for title in state["outline"]:
        content = state["sections_content"].get(title, "")
        parts.append(f"{title}\n{content}")
    full_srs = "\n\n".join(parts)
    # 可选：添加封面或修订历史
    return {"final_srs": full_srs}