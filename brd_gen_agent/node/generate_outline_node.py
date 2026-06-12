
from langchain_core.messages import HumanMessage
from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node
from brd_gen_agent.utils.llm import deepseek_llm

from typing import List, Dict
import re


def parse_template_sections(template: str) -> List[Dict[str, str]]:
    """解析模板中的各章节标题和填写要求。"""
    section_pattern = re.compile(r'^(#{2,3})\s+(.+)$', re.MULTILINE)
    sections = []
    matches = list(section_pattern.finditer(template))
    for i, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()
        heading = f"{'#' * level} {title}"
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(template)
        instruction = template[start:end].strip()
        sections.append({
            "heading": heading,
            "title": title,
            "level": level,
            "instruction": instruction
        })
    return sections


@logged_node
def generate_outline_node(state: SRSState, config=None) -> SRSState:
    template_sections = parse_template_sections(state["template_content"])
    titles = [section['heading'] for section in template_sections]

    if not titles:
        # 如果模板中没有标题，则使用 LLM 从模板内容中生成大纲
        prompt = f"""你是一位资深需求分析师。请根据以下提供的模板，生成一份《需求规格说明书》的详细大纲。
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

"""
        response = deepseek_llm.invoke([HumanMessage(content=prompt)])
        titles = re.findall(r'^(#{2,3}\s+.+)$', response.content, re.MULTILINE)

    return {
        "outline": titles,
        "template_sections": template_sections,
        "sections_content": {}
    }

