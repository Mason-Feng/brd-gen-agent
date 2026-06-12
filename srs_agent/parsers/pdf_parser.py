"""
PDF文档解析器
使用 PyMuPDF (fitz) 进行解析
"""

from typing import Dict, Any
import fitz  # PyMuPDF


def parse_pdf(file_path: str) -> Dict[str, Any]:
    """
    解析PDF文件
    
    Args:
        file_path: PDF文件路径
        
    Returns:
        包含解析结果的字典
    """
    try:
        doc = fitz.open(file_path)
        
        # 提取文本内容
        full_text = []
        for page in doc:
            text = page.get_text()
            if text:
                full_text.append(text)
        
        content = '\n'.join(full_text)
        
        # 提取元数据
        metadata = {
            'page_count': len(doc),
        }
        
        doc.close()
        
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
