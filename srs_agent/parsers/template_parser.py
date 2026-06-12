"""
SRS模板解析器
解析SRS模板文件，提取章节结构
"""

from typing import List
import re
from srs_agent.graph.state import Section


def parse_template(template_text: str) -> List[Section]:
    """
    解析SRS模板文本，提取章节结构和要求
    
    Args:
        template_text: 模板文本内容
        
    Returns:
        章节列表（包含章节要求）
    """
    sections = []
    lines = template_text.split('\n')
    
    current_section = None
    current_requirements = []
    
    for line in lines:
        # 匹配Markdown标题格式: # 1 引言, ## 2.1 功能描述
        match = re.match(r'^(#{1,6})\s+(\d+(?:\.\d+)*)\s+(.+)$', line.strip())
        
        if match:
            # 如果之前有正在处理的章节，先保存它
            if current_section is not None:
                current_section.requirements = '\n'.join(current_requirements).strip()
                sections.append(current_section)
            
            hashes = match.group(1)
            section_id = match.group(2)
            title = match.group(3)
            level = len(hashes)
            
            # 创建新章节
            current_section = Section(
                id=section_id,
                title=title,
                level=level
            )
            # 重置要求收集
            current_requirements = []
        elif current_section is not None:
            # 非标题行，作为当前章节的要求/描述
            stripped_line = line.strip()
            if stripped_line:  # 忽略空行
                current_requirements.append(stripped_line)
    
    # 处理最后一个章节
    if current_section is not None:
        current_section.requirements = '\n'.join(current_requirements).strip()
        sections.append(current_section)
    
    return sections


def parse_template_from_file(file_path: str) -> List[Section]:
    """
    从文件解析SRS模板
    
    Args:
        file_path: 模板文件路径
        
    Returns:
        章节列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        template_text = f.read()
    
    return parse_template(template_text)
