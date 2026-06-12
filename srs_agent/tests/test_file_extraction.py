"""
测试文件提取节点
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agents.file_extraction_agent import file_extraction_node
from graph.state import SRSState

def test_file_extraction():
    """测试文件提取节点"""
    
    print("=" * 80)
    print("测试文件提取节点")
    print("=" * 80)
    print()
    
    # 创建测试状态
    test_state: SRSState = {
        'project_dir': '',
        'input_files': [
            os.path.join(os.path.dirname(__file__), '..', 'tests', 'test_data', 'test_document.md')
        ],
        'parsed_documents': [],
        'project_memory': {},
        'topic_graph': {},
        'template_path': '',
        'template_sections': [],
        'current_section_index': 0,
        'section_plan': {},
        'current_evidences': [],
        'sections_content': {},
        'review_comments': [],
        'needs_revision': False,
        'output_path': '',
        'final_markdown': '',
        'errors': []
    }
    
    try:
        # 执行文件提取节点
        result_state = file_extraction_node(test_state)
        
        # 检查结果
        parsed_docs = result_state.get('parsed_documents', [])
        
        print(f"✅ 文件提取成功！")
        print(f"   解析了 {len(parsed_docs)} 个文档")
        print()
        
        if parsed_docs:
            doc = parsed_docs[0]
            print(f"文档信息:")
            print(f"  - 文件名: {doc.file_name}")
            print(f"  - 文件类型: {doc.file_type}")
            print(f"  - 内容长度: {len(doc.content)} 字符")
            print(f"  - 元数据: {doc.metadata}")
            print()
            
            # 显示部分内容
            preview = doc.content[:200].replace('\n', ' ')
            print(f"内容预览: {preview}...")
            print()
        
        # 检查是否有错误
        errors = result_state.get('errors', [])
        if errors:
            print(f"⚠️  警告: 发现 {len(errors)} 个错误:")
            for error in errors:
                print(f"   - {error}")
            print()
        
        print("=" * 80)
        print("✅ 测试完成！")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_file_extraction()
    sys.exit(0 if success else 1)
