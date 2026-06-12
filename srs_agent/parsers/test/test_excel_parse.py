import sys
import os

# 将项目根目录添加到 Python 路径中，以便能够识别 srs_agent 包
# 当前文件路径: D:\project\brd-gen-agent\srs_agent\parsers\test\test_temp_parse.py
# 项目根目录: D:\project\brd-gen-agent
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from srs_agent.parsers import excel_parser

if __name__ == '__main__':
    excel_file_path=r'D:\project\brd-gen-agent\测试文件\受益人业务相关文档\相关参考文档\界面\界面原型\报表表样（共计8张）.xlsx'
    parse_result=excel_parser.parse_excel(excel_file_path)
    print(parse_result)