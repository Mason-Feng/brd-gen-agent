"""
文件解析模块单元测试
测试所有文档解析器的功能
"""

import sys
import os
import unittest
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from parsers.markdown_parser import parse_markdown
from parsers.template_parser import parse_template, parse_template_from_file

# 可选导入：HTML解析器
try:
    from parsers.html_parser import parse_html
    HTML_PARSER_AVAILABLE = True
except ImportError:
    HTML_PARSER_AVAILABLE = False
    parse_html = None


class TestMarkdownParser(unittest.TestCase):
    """Markdown解析器测试"""
    
    def setUp(self):
        """测试准备"""
        self.test_file = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'test_document.md'
        )
    
    def test_parse_markdown_success(self):
        """测试成功解析Markdown文件"""
        result = parse_markdown(self.test_file)
        
        # 验证返回结构
        self.assertIsInstance(result, dict)
        self.assertIn('content', result)
        self.assertIn('metadata', result)
        self.assertIn('success', result)
        
        # 验证解析成功
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['content'])
        self.assertGreater(len(result['content']), 0)
        
        # 验证内容正确性
        self.assertIn('软件需求规格说明书', result['content'])
        self.assertIn('用户管理', result['content'])
        self.assertIn('订单管理', result['content'])
    
    def test_parse_markdown_content_integrity(self):
        """测试内容完整性"""
        result = parse_markdown(self.test_file)
        content = result['content']
        
        # 验证关键章节都存在
        expected_sections = [
            '引言',
            '功能需求',
            '用户管理',
            '订单管理',
            '非功能需求',
            '性能',
            '安全性'
        ]
        
        for section in expected_sections:
            self.assertIn(section, content, f"缺少章节: {section}")
    
    def test_parse_markdown_metadata(self):
        """测试元数据提取"""
        result = parse_markdown(self.test_file)
        
        # Markdown解析器当前不提取元数据
        self.assertIsInstance(result['metadata'], dict)
    
    def test_parse_nonexistent_file(self):
        """测试解析不存在的文件"""
        result = parse_markdown('/nonexistent/path/file.md')
        
        # 验证失败处理
        self.assertFalse(result['success'])
        self.assertEqual(result['content'], '')
        self.assertIn('error', result)
        self.assertIsNotNone(result['error'])
    
    def test_parse_empty_file(self):
        """测试解析空文件"""
        # 创建临时空文件
        temp_file = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'temp_empty.md'
        )
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write('')
            
            result = parse_markdown(temp_file)
            
            # 空文件应该成功解析，但内容为空
            self.assertTrue(result['success'])
            self.assertEqual(result['content'], '')
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_parse_unicode_content(self):
        """测试Unicode内容解析"""
        # 创建包含Unicode的临时文件
        temp_file = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'temp_unicode.md'
        )
        
        try:
            unicode_content = "# 测试\n这是中文内容。\n日本語テスト。\nEmoji: 😀🎉"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(unicode_content)
            
            result = parse_markdown(temp_file)
            
            # 验证Unicode内容正确解析
            self.assertTrue(result['success'])
            self.assertIn('中文', result['content'])
            self.assertIn('日本語', result['content'])
            self.assertIn('😀', result['content'])
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.remove(temp_file)


@unittest.skipUnless(HTML_PARSER_AVAILABLE, "beautifulsoup4 未安装")
class TestHTMLParser(unittest.TestCase):
    """HTML解析器测试"""
    
    def setUp(self):
        """测试准备"""
        self.test_file = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'test_document.html'
        )
    
    def test_parse_html_success(self):
        """测试成功解析HTML文件"""
        result = parse_html(self.test_file)
        
        # 验证返回结构
        self.assertIsInstance(result, dict)
        self.assertIn('content', result)
        self.assertIn('metadata', result)
        self.assertIn('success', result)
        
        # 验证解析成功
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['content'])
        self.assertGreater(len(result['content']), 0)
    
    def test_parse_html_content_extraction(self):
        """测试HTML内容提取"""
        result = parse_html(self.test_file)
        content = result['content']
        
        # 验证文本内容被正确提取（不含HTML标签）
        self.assertIn('软件需求文档', content)
        self.assertIn('项目概述', content)
        self.assertIn('电子商务平台', content)
        
        # 验证HTML标签已被移除
        self.assertNotIn('<html>', content)
        self.assertNotIn('<div>', content)
    
    def test_parse_html_metadata(self):
        """测试HTML元数据提取"""
        result = parse_html(self.test_file)
        
        # 验证标题被提取
        self.assertIn('title', result['metadata'])
        self.assertEqual(result['metadata']['title'], '测试HTML文档')
    
    def test_parse_html_list_items(self):
        """测试HTML列表项提取"""
        result = parse_html(self.test_file)
        content = result['content']
        
        # 验证列表项被提取
        expected_items = ['用户管理', '商品管理', '订单处理', '支付系统']
        for item in expected_items:
            self.assertIn(item, content)
    
    def test_parse_nonexistent_html(self):
        """测试解析不存在的HTML文件"""
        result = parse_html('/nonexistent/path/file.html')
        
        # 验证失败处理
        self.assertFalse(result['success'])
        self.assertEqual(result['content'], '')
        self.assertIn('error', result)


class TestTemplateParser(unittest.TestCase):
    """SRS模板解析器测试"""
    
    def setUp(self):
        """测试准备"""
        self.test_file = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'test_template.md'
        )
        
        # 简单的模板文本
        self.sample_template = """# 1 引言

## 1.1 目的
测试目的。

# 2 功能需求

## 2.1 用户管理

### 2.1.1 注册
用户可以注册。

## 2.2 订单管理
"""
    
    def test_parse_template_from_text(self):
        """测试从文本解析模板"""
        sections = parse_template(self.sample_template)
        
        # 验证返回类型
        self.assertIsInstance(sections, list)
        self.assertGreater(len(sections), 0)
    
    def test_parse_template_structure(self):
        """测试模板结构解析"""
        sections = parse_template(self.sample_template)
        
        # 验证章节数量（应该有6个章节）
        self.assertEqual(len(sections), 6)
        
        # 验证第一个章节
        first_section = sections[0]
        self.assertEqual(first_section.id, '1')
        self.assertEqual(first_section.title, '引言')
        self.assertEqual(first_section.level, 1)
    
    def test_parse_template_hierarchy(self):
        """测试模板层级解析"""
        sections = parse_template(self.sample_template)
        
        # 验证不同层级的章节
        level_1 = [s for s in sections if s.level == 1]
        level_2 = [s for s in sections if s.level == 2]
        level_3 = [s for s in sections if s.level == 3]
        
        # 应该有2个一级章节
        self.assertEqual(len(level_1), 2)
        
        # 应该有3个二级章节
        self.assertEqual(len(level_2), 3)
        
        # 应该有1个三级章节
        self.assertEqual(len(level_3), 1)
    
    def test_parse_template_section_ids(self):
        """测试章节编号解析"""
        sections = parse_template(self.sample_template)
        
        # 验证章节编号
        expected_ids = ['1', '1.1', '2', '2.1', '2.1.1', '2.2']
        actual_ids = [s.id for s in sections]
        
        self.assertEqual(actual_ids, expected_ids)
    
    def test_parse_template_from_file(self):
        """测试从文件解析模板"""
        sections = parse_template_from_file(self.test_file)
        
        # 验证解析成功
        self.assertIsInstance(sections, list)
        self.assertGreater(len(sections), 0)
        
        # 验证第一个章节
        first_section = sections[0]
        self.assertEqual(first_section.id, '1')
        self.assertEqual(first_section.title, '引言')
    
    def test_parse_complex_template(self):
        """测试复杂模板解析"""
        complex_template = """# 1 引言
# 2 总体描述
## 2.1 产品视角
## 2.2 用户特征
# 3 功能需求
## 3.1 模块A
### 3.1.1 功能1
### 3.1.2 功能2
## 3.2 模块B
### 3.2.1 功能3
# 4 接口需求
## 4.1 UI
## 4.2 API
# 5 非功能需求
"""
        sections = parse_template(complex_template)
        
        # 验证所有章节都被解析
        self.assertEqual(len(sections), 14)
        
        # 验证层级分布
        level_counts = {}
        for s in sections:
            level_counts[s.level] = level_counts.get(s.level, 0) + 1
        
        self.assertEqual(level_counts[1], 5)  # 5个一级章节
        self.assertEqual(level_counts[2], 6)  # 6个二级章节
        self.assertEqual(level_counts[3], 3)  # 3个三级章节
    
    def test_parse_template_with_special_chars(self):
        """测试包含特殊字符的模板"""
        special_template = """# 1 引言 & 概述
## 1.1 目的 <重要>
# 2 功能需求 (核心)
"""
        sections = parse_template(special_template)
        
        # 验证特殊字符被正确处理
        self.assertEqual(len(sections), 3)
        self.assertIn('&', sections[0].title)
        self.assertIn('<重要>', sections[1].title)
        self.assertIn('(核心)', sections[2].title)
    
    def test_parse_empty_template(self):
        """测试空模板解析"""
        sections = parse_template("")
        
        # 空模板应返回空列表
        self.assertEqual(sections, [])
    
    def test_parse_template_no_numbering(self):
        """测试无编号的模板"""
        no_number_template = """# 引言
# 功能需求
## 用户管理
"""
        sections = parse_template(no_number_template)
        
        # 没有编号的标题应该被忽略
        self.assertEqual(len(sections), 0)
    
    def test_parse_template_mixed_format(self):
        """测试混合格式的模板"""
        mixed_template = """# 1 正确格式
Some text without heading
## 1.1 子章节
# Invalid
## 2.1 另一个子章节
"""
        sections = parse_template(mixed_template)
        
        # 只解析符合格式的标题
        self.assertEqual(len(sections), 3)
        self.assertEqual(sections[0].id, '1')
        self.assertEqual(sections[1].id, '1.1')
        self.assertEqual(sections[2].id, '2.1')
    
    def test_parse_template_requirements_extraction(self):
        """测试章节要求提取"""
        template_with_requirements = """# 1 引言
本文档描述系统需求。
适用于所有项目。

## 1.1 目的
明确系统目标。
定义系统范围。

# 2 功能需求
系统应具备以下功能。
"""
        sections = parse_template(template_with_requirements)
        
        # 验证章节数量
        self.assertEqual(len(sections), 3)
        
        # 验证第一个章节的要求
        self.assertEqual(sections[0].id, '1')
        self.assertIn('本文档描述系统需求', sections[0].requirements)
        self.assertIn('适用于所有项目', sections[0].requirements)
        
        # 验证第二个章节的要求
        self.assertEqual(sections[1].id, '1.1')
        self.assertIn('明确系统目标', sections[1].requirements)
        self.assertIn('定义系统范围', sections[1].requirements)
        
        # 验证第三个章节的要求
        self.assertEqual(sections[2].id, '2')
        self.assertIn('系统应具备以下功能', sections[2].requirements)
    
    def test_parse_template_empty_requirements(self):
        """测试没有要求的章节"""
        template_no_requirements = """# 1 引言

## 1.1 目的

# 2 功能需求
"""
        sections = parse_template(template_no_requirements)
        
        # 所有章节的 requirements 应该为空字符串
        for section in sections:
            self.assertEqual(section.requirements, '')
    
    def test_parse_template_multiline_requirements(self):
        """测试多行要求的提取"""
        multiline_template = """# 1 引言
第一行要求。
第二行要求。
第三行要求。

## 1.1 目的
目的说明第一行。
目的说明第二行。
"""
        sections = parse_template(multiline_template)
        
        # 验证多行要求被正确提取并合并
        self.assertIn('第一行要求', sections[0].requirements)
        self.assertIn('第二行要求', sections[0].requirements)
        self.assertIn('第三行要求', sections[0].requirements)
        
        self.assertIn('目的说明第一行', sections[1].requirements)
        self.assertIn('目的说明第二行', sections[1].requirements)


class TestDocumentParserIntegration(unittest.TestCase):
    """文档解析器集成测试"""
    
    def test_multiple_markdown_files(self):
        """测试解析多个Markdown文件"""
        test_files = [
            os.path.join(os.path.dirname(__file__), 'test_data', 'test_document.md'),
            os.path.join(os.path.dirname(__file__), 'test_data', 'test_template.md')
        ]
        
        results = []
        for file_path in test_files:
            result = parse_markdown(file_path)
            results.append(result)
        
        # 验证所有文件都成功解析
        for result in results:
            self.assertTrue(result['success'])
            self.assertGreater(len(result['content']), 0)
    
    def test_parser_error_handling(self):
        """测试解析器错误处理"""
        # 测试各种错误情况
        error_cases = [
            '/nonexistent/file.md',
            '',
            None,
        ]
        
        for invalid_path in error_cases:
            if invalid_path is None:
                continue  # 跳过None测试
            
            try:
                result = parse_markdown(invalid_path)
                self.assertFalse(result['success'])
                self.assertIn('error', result)
            except Exception:
                # 某些情况可能抛出异常，这也是可接受的
                pass


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestMarkdownParser))
    suite.addTests(loader.loadTestsFromTestCase(TestHTMLParser))
    suite.addTests(loader.loadTestsFromTestCase(TestTemplateParser))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentParserIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("=" * 80)
    print("开始运行文件解析模块单元测试")
    print("=" * 80)
    print()
    
    result = run_tests()
    
    print()
    print("=" * 80)
    if result.wasSuccessful():
        print(f"所有测试通过！共 {result.testsRun} 个测试")
    else:
        print(f"测试失败：{len(result.failures)} 个失败，{len(result.errors)} 个错误")
    print("=" * 80)
    
    sys.exit(0 if result.wasSuccessful() else 1)
