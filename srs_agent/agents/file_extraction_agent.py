"""
文件提取代理 - File Extraction Agent
负责加载和解析各种格式的输入文件，提取文本内容
"""

from typing import List
from graph.state import SRSState, ParsedDocument
from parsers.document_parser import parse_document
from utils.logger import log_node_execution


@log_node_execution
def file_extraction_node(state: SRSState) -> SRSState:
    """
    文件提取代理节点
    
    功能：
    1. 读取输入文件路径列表
    2. 根据文件类型选择合适的解析器
    3. 解析文件并提取文本内容
    4. 构建统一的ParsedDocument对象
    
    Args:
        state: 当前状态
        
    Returns:
        更新后的状态
        
    支持的文件格式：
    - PDF (.pdf)
    - Word (.docx)
    - Excel (.xlsx, .xls)
    - PowerPoint (.pptx, .ppt)
    - Markdown (.md)
    - HTML (.html, .htm)
    - 图片 (.png, .jpg, .jpeg) - OCR识别
    """
    try:
        # 从状态中获取输入文件路径
        input_files = state.get('input_files', [])
        project_dir = state.get('project_dir', '')
        
        if not input_files:
            raise ValueError("未指定输入文件列表")
        
        # 解析所有文件
        parsed_documents: List[ParsedDocument] = []
        
        for file_path in input_files:
            # 如果是相对路径，拼接项目目录
            if not os.path.isabs(file_path) and project_dir:
                file_path = os.path.join(project_dir, file_path)
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                error_msg = f"文件不存在: {file_path}"
                if 'errors' not in state:
                    state['errors'] = []
                state['errors'].append(error_msg)
                continue
            
            try:
                # 解析文档
                parsed_doc = parse_document(file_path)
                parsed_documents.append(parsed_doc)
                
            except Exception as e:
                # 记录单个文件解析错误，但继续处理其他文件
                error_msg = f"解析文件失败 [{file_path}]: {str(e)}"
                if 'errors' not in state:
                    state['errors'] = []
                state['errors'].append(error_msg)
        
        # 检查是否有成功解析的文档
        if not parsed_documents:
            raise ValueError("所有文件解析失败，无可用文档")
        
        # 更新状态
        state['parsed_documents'] = parsed_documents
        
    except Exception as e:
        if 'errors' not in state:
            state['errors'] = []
        state['errors'].append(f"文件提取失败: {str(e)}")
        raise  # 重新抛出异常，让装饰器记录
    
    return state


# 需要导入os模块
import os
