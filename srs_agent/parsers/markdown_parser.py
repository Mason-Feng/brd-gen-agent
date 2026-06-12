"""
Markdown文档解析器
"""

from typing import Dict, Any


def parse_markdown(file_path: str) -> Dict[str, Any]:
    """
    解析Markdown文件
    
    Args:
        file_path: Markdown文件路径
        
    Returns:
        包含解析结果的字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 提取元数据
        metadata = {}
        
        return {
            'content': content,
            'metadata': metadata,
            'success': True
        }
    except Exception as e:
        return {
            'content': '',
            'metadata': {},
            'success': False,
            'error': str(e)
        }
