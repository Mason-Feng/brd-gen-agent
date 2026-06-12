import unittest
from brd_gen_agent.node.generate_outline_node import parse_template_sections


class TestParseTemplateSections(unittest.TestCase):
    """Test suite for parse_template_sections function"""

    def test_parse_simple_template(self):
        """Test parsing a simple template with basic sections"""
        template = """## 1. 引言
这是引言部分
### 1.1 目的
说明项目目的
## 2. 总体描述
系统总体描述
"""
        result = parse_template_sections(template)
        
        self.assertEqual(len(result), 3)
        
        # Check first section
        self.assertEqual(result[0]["heading"], "## 1. 引言")
        self.assertEqual(result[0]["title"], "1. 引言")
        self.assertEqual(result[0]["level"], 2)
        self.assertIn("这是引言部分", result[0]["instruction"])
        
        # Check second section (subsection)
        self.assertEqual(result[1]["heading"], "### 1.1 目的")
        self.assertEqual(result[1]["title"], "1.1 目的")
        self.assertEqual(result[1]["level"], 3)
        self.assertIn("说明项目目的", result[1]["instruction"])
        
        # Check third section
        self.assertEqual(result[2]["heading"], "## 2. 总体描述")
        self.assertEqual(result[2]["title"], "2. 总体描述")
        self.assertEqual(result[2]["level"], 2)
        self.assertIn("系统总体描述", result[2]["instruction"])

    def test_parse_template_with_multiline_instructions(self):
        """Test parsing template with multi-line instructions"""
        template = """## 1. 需求分析
请提供以下内容：
- 功能需求
- 非功能需求
- 约束条件

### 1.1 功能需求
详细描述系统的功能需求，包括：
1. 核心功能
2. 辅助功能
3. 扩展功能
"""
        result = parse_template_sections(template)
        
        self.assertEqual(len(result), 2)
        self.assertIn("功能需求", result[0]["instruction"])
        self.assertIn("非功能需求", result[0]["instruction"])
        self.assertIn("约束条件", result[0]["instruction"])

    def test_parse_empty_template(self):
        """Test parsing an empty template"""
        template = ""
        result = parse_template_sections(template)
        
        self.assertEqual(len(result), 0)

    def test_parse_template_without_sections(self):
        """Test parsing a template without markdown sections"""
        template = """这是一个没有标题的模板
只包含普通文本内容
没有任何markdown标题
"""
        result = parse_template_sections(template)
        
        self.assertEqual(len(result), 0)

    def test_parse_template_with_only_level2_headers(self):
        """Test parsing template with only level 2 headers"""
        template = """## 第一章
内容一
## 第二章
内容二
## 第三章
内容三
"""
        result = parse_template_sections(template)
        
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertEqual(item["level"], 2)
            self.assertIn("#", item["heading"])

    def test_parse_template_with_only_level3_headers(self):
        """Test parsing template with only level 3 headers"""
        template = """### 小节1
内容1
### 小节2
内容2
"""
        result = parse_template_sections(template)
        
        self.assertEqual(len(result), 2)
        for item in result:
            self.assertEqual(item["level"], 3)

    def test_parse_template_with_mixed_headers(self):
        """Test parsing template with mixed level 2 and level 3 headers"""
        template = """## 第一章
章级内容
### 第一节
节级内容
### 第二节
更多内容
## 第二章
第二章内容
"""
        result = parse_template_sections(template)
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["level"], 2)
        self.assertEqual(result[1]["level"], 3)
        self.assertEqual(result[2]["level"], 3)
        self.assertEqual(result[3]["level"], 2)

    def test_parse_template_section_instruction_extraction(self):
        """Test that instructions are correctly extracted until next section"""
        template = """## 部分A
这是A的说明
第一行
第二行
### 子部分A1
这是A1的说明
最后一行
## 部分B
这是B的说明
"""
        result = parse_template_sections(template)
        
        # The instruction for "部分A" should include everything until the next section
        self.assertIn("这是A的说明", result[0]["instruction"])
        self.assertIn("第一行", result[0]["instruction"])
        self.assertIn("第二行", result[0]["instruction"])
        
        # The instruction for "子部分A1" should include its content until the next section
        self.assertIn("这是A1的说明", result[1]["instruction"])

    def test_parse_template_with_special_characters_in_titles(self):
        """Test parsing template with special characters in titles"""
        template = """## 1.1 用户需求（一期）
相关内容
## 1.2 系统需求 & 约束
更多内容
"""
        result = parse_template_sections(template)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "1.1 用户需求（一期）")
        self.assertEqual(result[1]["title"], "1.2 系统需求 & 约束")

    def test_parse_template_ignores_level1_headers(self):
        """Test that level 1 headers (single #) are ignored"""
        template = """# 这是一级标题（应该被忽略）
一些内容
## 二级标题
二级内容
"""
        result = parse_template_sections(template)
        
        # Should only match level 2 and 3 headers
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["level"], 2)

    def test_parse_template_ignores_level4plus_headers(self):
        """Test that level 4+ headers are ignored"""
        template = """## 二级标题
内容
#### 四级标题
应该被忽略
##### 五级标题
也应该被忽略
"""
        result = parse_template_sections(template)
        
        # Should only match level 2 header
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "二级标题")


if __name__ == "__main__":
    unittest.main()
