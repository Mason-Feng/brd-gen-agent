
from langchain_core.messages import HumanMessage, SystemMessage
from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node
from brd_gen_agent.utils.llm import deepseek_llm

@logged_node
def generate_outline_node(state: SRSState, config=None) -> SRSState:
    prompt = f"""你是一位资深需求分析师。请根据以下业务文档上下文和提供的模板，生成一份《需求规格说明书》的详细大纲。
要求：
1. 大纲必须采用 Markdown 标题格式，仅使用 ## 和 ### 级别的标题，不要包含具体内容。
2. 大纲应当覆盖模板中的所有章节，并可以根据上下文增加具体的业务小节。
3. 输出格式为纯文本，每行一个标题，例如：
## 1. 引言
### 1.1 目的
### 1.2 范围
...
## 2. 总体描述
...

模板内容：
{state["template_content"]}

业务上下文（部分）：
{state["context_text"][:3000]}  # 只给前部分避免过长
"""
    response = deepseek_llm.invoke([HumanMessage(content=prompt)])
    # 解析出标题行
    import re
    titles = re.findall(r'^(#{2,3}\s+.+)$', response.content, re.MULTILINE)
    if not titles:
        # 降级：直接使用模板中的标题
        titles = re.findall(r'^(#{2,3}\s+.+)$', state["template_content"], re.MULTILINE)
    return {"outline": titles, "sections_content": {}}

