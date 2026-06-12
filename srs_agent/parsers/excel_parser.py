"""
Excel文档解析器
"""

from typing import Dict, Any
import pandas as pd


def parse_excel(file_path: str) -> Dict[str, Any]:
    """
    解析Excel文件
    
    Args:
        file_path: Excel文件路径
        
    Returns:
        包含解析结果的字典
    """
    try:
        # 读取所有sheet
        excel_file = pd.ExcelFile(file_path)
        
        all_sheets = {}
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            all_sheets[sheet_name] = df.to_string(index=False)
        
        # 合并所有内容
        content = '\n\n'.join([f"Sheet: {name}\n{text}" 
                               for name, text in all_sheets.items()])
        
        # 提取元数据
        metadata = {
            'sheet_count': len(excel_file.sheet_names),
            'sheets': excel_file.sheet_names,
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
