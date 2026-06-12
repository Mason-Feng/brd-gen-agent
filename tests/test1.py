
import sys
from pathlib import Path

# Ensure project root is on sys.path so `brd_gen_agent` can be imported
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from brd_gen_agent.node.generate_outline_node import parse_template_sections


if __name__ == "__main__":
    # Read the template file content instead of passing a file path string
    tpl_path = Path(r"D:\project\brd-gen-agent\测试文件\业务需求规格说明书模板.md")
    if not tpl_path.exists():
        print(f"Template file not found: {tpl_path}")
        sys.exit(1)

    template_text = tpl_path.read_text(encoding="utf-8")
    result = parse_template_sections(template_text)
    print(result)