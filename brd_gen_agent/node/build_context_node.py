from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node
@logged_node
def build_context_node(state: SRSState, config=None) -> SRSState:
    parts = []
    for doc in state["documents"]:
        parts.append(f"[文件] {doc['path']}\n```\n{doc['content']}\n```")
    context = "\n\n".join(parts)
    # 若上下文过长（超过 100K 字符），可简单截断，或后续引入 RAG
    MAX_CHARS = 80000  # 约 20K tokens (中文)，可根据模型窗口调整
    if len(context) > MAX_CHARS:
        context = context[:MAX_CHARS] + "\n... (内容截断)"
    return {"context_text": context}