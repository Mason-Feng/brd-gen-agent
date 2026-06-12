"""
图像文档解析器（OCR）
"""

from typing import Dict, Any
import pytesseract
from PIL import Image


def parse_image(file_path: str) -> Dict[str, Any]:
    """
    解析图像文件（使用OCR提取文本）
    
    Args:
        file_path: 图像文件路径
        
    Returns:
        包含解析结果的字典
    """
    try:
        # 打开图像
        image = Image.open(file_path)
        
        # 使用OCR提取文本
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        
        # 提取元数据
        metadata = {
            'size': image.size,
            'format': image.format,
        }
        
        return {
            'content': text,
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
