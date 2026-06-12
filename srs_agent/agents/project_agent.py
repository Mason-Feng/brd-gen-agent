"""
项目代理 - Project Agent
负责从解析后的文档中提取项目全量知识，构建Project Memory
"""

from graph.state import SRSState
from memory.project_memory import ProjectMemory
from utils.logger import log_node_execution


@log_node_execution
def project_agent_node(state: SRSState) -> SRSState:
    """
    项目代理节点
    
    功能：
    1. 分析所有解析后的文档
    2. 提取项目知识（角色、模块、实体、API等）
    3. 构建Project Memory
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
    """
    try:
        # 获取解析后的文档
        parsed_documents = state.get('parsed_documents', [])
        if not parsed_documents:
            raise ValueError("没有可分析的文档")
        
        # 创建Project Memory
        project_memory = ProjectMemory()
        
        # TODO: 这里应该调用LLM进行知识提取
        # 目前使用简单规则提取作为示例
        for doc in parsed_documents:
            # 示例：从文件名推测项目名称
            if not project_memory.data.project_name:
                project_memory.set_project_name(doc.file_name.replace('.docx', '').replace('.pdf', ''))
            
            # 示例：从内容中提取关键词（简化版）
            content_lower = doc.content.lower()
            
            # 检测用户角色
            if '管理员' in doc.content:
                project_memory.add_role('管理员')
            if '用户' in doc.content:
                project_memory.add_role('普通用户')
            
            # 检测功能模块（示例）
            if '管理' in doc.content:
                project_memory.add_module('管理模块')
            
            # 实际应用中应该使用LLM进行更智能的提取
        
        # 将Project Memory转换为字典并存入状态
        state['project_memory'] = project_memory.to_dict()
        
    except Exception as e:
        if 'errors' not in state:
            state['errors'] = []
        state['errors'].append(f"项目知识提取失败: {str(e)}")
    
    return state
