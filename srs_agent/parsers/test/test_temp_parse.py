import sys
import os

# 将项目根目录添加到 Python 路径中，以便能够识别 srs_agent 包
# 当前文件路径: D:\project\brd-gen-agent\srs_agent\parsers\test\test_temp_parse.py
# 项目根目录: D:\project\brd-gen-agent
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from srs_agent.parsers import template_parser

if __name__ == '__main__':
    template_file_path=r'D:\project\brd-gen-agent\测试文件\业务需求规格说明书模板.md'
    parse_result=template_parser.parse_template_from_file(template_file_path)
    print(parse_result)