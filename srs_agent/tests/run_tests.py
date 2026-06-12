"""
测试运行器 - 自动检测依赖并运行可用的测试
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def check_dependencies():
    """检查测试依赖"""
    dependencies = {
        'bs4': 'beautifulsoup4 (HTML解析)',
        'docx': 'python-docx (DOCX解析)',
        'fitz': 'pymupdf (PDF解析)',
        'pandas': 'pandas (Excel解析)',
        'pptx': 'python-pptx (PPT解析)',
    }
    
    missing = []
    available = []
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            available.append(description)
        except ImportError:
            missing.append(description)
    
    return available, missing


def run_markdown_tests():
    """运行Markdown解析器测试"""
    print("\n" + "="*80)
    print("📝 运行 Markdown 解析器测试")
    print("="*80)
    
    from tests.test_parsers import TestMarkdownParser
    import unittest
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMarkdownParser)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def run_template_tests():
    """运行模板解析器测试"""
    print("\n" + "="*80)
    print("📋 运行模板解析器测试")
    print("="*80)
    
    from tests.test_parsers import TestTemplateParser
    import unittest
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplateParser)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def run_html_tests():
    """运行HTML解析器测试（需要beautifulsoup4）"""
    print("\n" + "="*80)
    print("🌐 运行 HTML 解析器测试")
    print("="*80)
    
    try:
        from bs4 import BeautifulSoup
        from tests.test_parsers import TestHTMLParser
        import unittest
        
        suite = unittest.TestLoader().loadTestsFromTestCase(TestHTMLParser)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result
    except ImportError:
        print("⚠️  跳过HTML测试：缺少 beautifulsoup4 依赖")
        print("   安装命令: pip install beautifulsoup4 lxml")
        return None


def main():
    """主函数"""
    print("\n" + "🧪"*40)
    print("SRS Agent 文件解析模块单元测试")
    print("🧪"*40)
    
    # 检查依赖
    print("\n📦 检查依赖...")
    available, missing = check_dependencies()
    
    if available:
        print(f"\n✅ 可用依赖 ({len(available)}):")
        for dep in available:
            print(f"   - {dep}")
    
    if missing:
        print(f"\n❌ 缺失依赖 ({len(missing)}):")
        for dep in missing:
            print(f"   - {dep}")
    
    # 运行测试
    all_results = []
    
    # 1. Markdown测试（无需额外依赖）
    try:
        result = run_markdown_tests()
        all_results.append(('Markdown', result))
    except Exception as e:
        print(f"\n❌ Markdown测试失败: {e}")
    
    # 2. 模板测试（无需额外依赖）
    try:
        result = run_template_tests()
        all_results.append(('Template', result))
    except Exception as e:
        print(f"\n❌ 模板测试失败: {e}")
    
    # 3. HTML测试（需要beautifulsoup4）
    try:
        result = run_html_tests()
        if result:
            all_results.append(('HTML', result))
    except Exception as e:
        print(f"\n❌ HTML测试失败: {e}")
    
    # 汇总结果
    print("\n" + "="*80)
    print("📊 测试结果汇总")
    print("="*80)
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for name, result in all_results:
        if result:
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)
            
            status = "✅ 通过" if result.wasSuccessful() else "❌ 失败"
            print(f"\n{name} 测试:")
            print(f"  - 测试数: {result.testsRun}")
            print(f"  - 失败: {len(result.failures)}")
            print(f"  - 错误: {len(result.errors)}")
            print(f"  - 状态: {status}")
    
    print("\n" + "="*80)
    print(f"总计: {total_tests} 个测试")
    print(f"失败: {total_failures}")
    print(f"错误: {total_errors}")
    
    if total_failures == 0 and total_errors == 0:
        print("\n✅ 所有测试通过！")
    else:
        print(f"\n❌ 有 {total_failures + total_errors} 个测试未通过")
    
    print("="*80 + "\n")
    
    # 返回退出码
    return 0 if (total_failures == 0 and total_errors == 0) else 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
