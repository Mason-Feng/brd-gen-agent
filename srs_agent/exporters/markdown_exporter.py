"""
Markdown导出器 - 将SRS导出为Markdown格式
"""

from graph.state import SRSState
from typing import Dict, Any
import os
from utils.logger import log_node_execution


@log_node_execution
def export_to_markdown(state: SRSState) -> SRSState:
    """
    将SRS导出为Markdown格式
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    # TODO: 实现Markdown导出逻辑
    # 1. 根据大纲结构组织内容
    # 2. 格式化章节标题
    # 3. 插入证据引用
    # 4. 生成目录
    # 5. 保存到文件
    
    # 示例：创建输出目录和文件
    output_dir = os.path.dirname(state.get('output_path', 'output/srs.md'))
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # 这里应该实际生成Markdown内容
    # content = generate_markdown_content(state)
    # with open(state['output_path'], 'w', encoding='utf-8') as f:
    #     f.write(content)
    
    return state


def generate_markdown_content(state: SRSState) -> str:
    """
    生成Markdown内容
    
    Args:
        state: 当前状态
        
    Returns:
        Markdown格式的文档内容
    """
    lines = []
    
    # 添加标题
    project_info = state.get('project_info', {})
    lines.append(f"# {project_info.get('name', '软件需求规格说明书')}")
    lines.append("")
    
    # 添加目录
    lines.append("## 目录")
    lines.append("")
    
    # 添加各章节内容
    outline = state.get('outline', [])
    for section in outline:
        lines.append(f"## {section.title}")
        lines.append("")
        
        # 添加章节内容
        section_content = state.get('sections_content', {}).get(section.title, '')
        if section_content:
            lines.append(section_content)
            lines.append("")
        
        # 递归添加子章节
        for subsection in section.subsections:
            lines.append(f"### {subsection.title}")
            lines.append("")
            subsection_content = state.get('sections_content', {}).get(subsection.title, '')
            if subsection_content:
                lines.append(subsection_content)
                lines.append("")
    
    return '\n'.join(lines)
