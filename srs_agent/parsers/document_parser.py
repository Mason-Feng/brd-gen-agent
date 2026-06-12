"""
文档解析器统一接口
根据文件类型自动选择对应的解析器
"""

from typing import Dict, Any
import os
from graph.state import ParsedDocument


def parse_document(file_path: str) -> ParsedDocument:
    """
    统一文档解析入口
    
    Args:
        file_path: 文件路径
        
    Returns:
        ParsedDocument对象
    """
    # 获取文件扩展名
    _, ext = os.path.splitext(file_path)
    ext = ext.lower().lstrip('.')
    
    # 根据扩展名选择解析器
    if ext in ['docx']:
        from parsers.docx_parser import parse_docx
        result = parse_docx(file_path)
    elif ext in ['pdf']:
        from parsers.pdf_parser import parse_pdf
        result = parse_pdf(file_path)
    elif ext in ['xlsx', 'xls', 'csv']:
        from parsers.excel_parser import parse_excel
        result = parse_excel(file_path)
    elif ext in ['pptx', 'ppt']:
        from parsers.ppt_parser import parse_ppt
        result = parse_ppt(file_path)
    elif ext in ['md', 'markdown']:
        from parsers.markdown_parser import parse_markdown
        result = parse_markdown(file_path)
    elif ext in ['html', 'htm']:
        from parsers.html_parser import parse_html
        result = parse_html(file_path)
    elif ext in ['png', 'jpg', 'jpeg', 'bmp']:
        from parsers.image_parser import parse_image
        result = parse_image(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")
    
    # 检查解析是否成功
    if not result.get('success', False):
        raise Exception(f"文件解析失败: {result.get('error', '未知错误')}")
    
    # 构建统一的ParsedDocument对象
    return ParsedDocument(
        file_name=os.path.basename(file_path),
        file_type=ext,
        content=result['content'],
        metadata=result.get('metadata', {})
    )


def parse_documents(file_paths: list) -> list:
    """
    批量解析文档
    
    Args:
        file_paths: 文件路径列表
        
    Returns:
        ParsedDocument对象列表
    """
    documents = []
    for file_path in file_paths:
        try:
            doc = parse_document(file_path)
            documents.append(doc)
        except Exception as e:
            print(f"警告: 文件解析失败 {file_path}: {str(e)}")
    
    return documents
