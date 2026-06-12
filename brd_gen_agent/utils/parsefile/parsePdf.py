import sys
import pdfplumber
from pathlib import Path

def pdf_to_markdown(pdf_path):
    """
    将 PDF 解析为 Markdown 格式，保留段落和表格结构。
    返回字符串。
    """
    markdown_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_md = f"## 第 {i+1} 页\n\n"

            # 获取页面上所有单词（带坐标）
            words = page.extract_words(keep_blank_chars=True, use_text_flow=True)

            # 查找页面上的所有表格
            tables_found = page.find_tables()

            # 收集表格的边界框
            table_bboxes = [table.bbox for table in tables_found]

            # 判断一个单词是否落在任意表格内部
            def in_any_table(word):
                x0, top, x1, bottom = word['x0'], word['top'], word['x1'], word['bottom']
                for (tx0, ttop, tx1, tbottom) in table_bboxes:
                    if x0 >= tx0 and x1 <= tx1 and top >= ttop and bottom <= tbottom:
                        return True
                return False

            # 分离表格内外的单词
            non_table_words = [w for w in words if not in_any_table(w)]

            # 将非表格单词按行聚合（近似还原文本行）
            if non_table_words:
                lines = {}
                for w in non_table_words:
                    # 将纵坐标四舍五入到一位小数，作为行标识
                    top = round(w['top'], 1)
                    lines.setdefault(top, []).append(w['text'])
                sorted_lines = sorted(lines.items(), key=lambda x: x[0])
                text_lines = [" ".join(line[1]) for line in sorted_lines]
                page_text = "\n".join(text_lines)
            else:
                page_text = ""

            page_md += page_text + "\n\n"

            # 将表格转换为 Markdown 表格
            if tables_found:
                for table in tables_found:
                    table_data = table.extract()
                    if not table_data or len(table_data) < 1:
                        continue
                    headers = [cell if cell else "" for cell in table_data[0]]
                    rows = table_data[1:]
                    md_table = "| " + " | ".join(headers) + " |\n"
                    md_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                    for row in rows:
                        # 填充可能缺失的列，保持列数一致
                        filled_row = [cell if cell else "" for cell in row]
                        while len(filled_row) < len(headers):
                            filled_row.append("")
                        md_table += "| " + " | ".join(filled_row[:len(headers)]) + " |\n"
                    page_md += md_table + "\n\n"

            markdown_pages.append(page_md)

    full_markdown = f"# PDF 文档：{pdf_path}\n\n" + "\n".join(markdown_pages)
    return full_markdown

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python pdf_to_md.py <PDF文件路径>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    try:
        md = pdf_to_markdown(pdf_path)
        out_file = Path.cwd() / f"{Path(pdf_path).stem}_parsed.md"
        out_file.write_text(md, encoding='utf-8')
        print(f"已将解析结果保存到: {out_file}")
    except Exception as e:
        print(f"解析出错：{e}")