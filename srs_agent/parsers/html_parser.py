"""
HTML文档解析器
"""

from typing import Dict, Any
from bs4 import BeautifulSoup


def parse_html(file_path: str) -> Dict[str, Any]:
    """
    解析HTML文件
    
    Args:
        file_path: HTML文件路径
        
    Returns:
        包含解析结果的字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取文本内容
        content = soup.get_text(separator='\n', strip=True)
        
        # 提取元数据
        metadata = {
            'title': soup.title.string if soup.title else '',
        }
        
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
