
from pathlib import Path
import sys

# Ensure project root is on sys.path so `brd_gen_agent` can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from brd_gen_agent.utils.parsefile.parseXlsx import parse_xlsx_to_dict, dict_to_markdown_tables
import json


if __name__ == "__main__":
    # 获取文件路径
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("请输入 xlsx 文件路径：").strip().strip('"')

    if not file_path:
        print("未提供文件路径，程序退出。")
        sys.exit(1)

    # 解析为结构化字典
    try:
        data = parse_xlsx_to_dict(file_path)
    except Exception as e:
        print(f"解析失败：{e}")
        sys.exit(1)

    # 输出格式选择（可以通过第二个命令行参数指定，默认输出 JSON）
    output_format = "markdown"  # 可以改为 "markdown"
    if len(sys.argv) > 2:
        output_format = sys.argv[2].lower()

    if output_format == "markdown":
        md_output = dict_to_markdown_tables(data)
        out_file = Path.cwd() / 'parsed_business_documents.md'
        out_file.write_text(md_output, encoding='utf-8')
        print(f"已将 Markdown 输出保存到: {out_file}")
    else:
        # 输出 JSON，确保中文不转义，缩进便于阅读
        json_output = json.dumps(data, ensure_ascii=False, indent=2)
        out_file = Path.cwd() / 'parsed_business_documents.json'
        out_file.write_text(json_output, encoding='utf-8')
        print(f"已将 JSON 输出保存到: {out_file}")