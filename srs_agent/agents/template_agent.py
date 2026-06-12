"""
模板代理 - Template Agent
负责解析SRS模板，提取章节结构
"""

from graph.state import SRSState
from parsers.template_parser import parse_template_from_file
from utils.logger import log_node_execution


@log_node_execution
def template_agent_node(state: SRSState) -> SRSState:
    """
    模板代理节点
    
    功能：
    1. 读取SRS模板文件
    2. 解析模板结构
    3. 提取章节列表
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    try:
        # 从状态中获取模板路径
        template_path = state.get('template_path')
        if not template_path:
            raise ValueError("未指定模板文件路径")
        
        # 解析模板
        sections = parse_template_from_file(template_path)
        
        # 更新状态
        state['template_sections'] = sections
        state['current_section_index'] = 0
        
    except Exception as e:
        if 'errors' not in state:
            state['errors'] = []
        state['errors'].append(f"模板解析失败: {str(e)}")
        raise  # 重新抛出异常，让装饰器记录
    
    return state
