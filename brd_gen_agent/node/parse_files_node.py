import os
from pathlib import Path
from typing import List, Dict, Optional

from brd_gen_agent.state import SRSState
from brd_gen_agent.utils.log import logged_node

def parse_all_files(root_dir: str) -> List[Dict[str, str]]:
    """递归提取所有可识别的文本文件"""
    documents = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            file_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(file_path, root_dir)
            text = extract_text(file_path)
            if text is not None:
                documents.append({"path": rel_path, "content": text})
    return documents

def extract_text(file_path: str) -> Optional[str]:
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in ['.md', '.txt', '.py', '.java', '.js', '.ts', '.html', '.css', '.c', '.cpp', '.h', '.yaml', '.yml', '.json']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif ext == '.docx':
            from docx import Document
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            return None
    except Exception as e:
        # 遇到无法解析的文件可记录日志并跳过
        return None

@logged_node
def parse_files_node(state: SRSState) -> SRSState:
    docs = parse_all_files(state["folder_path"])
    if state.get("codebase_path"):
        docs.extend(parse_all_files(state["codebase_path"]))
    # 读取模板内容
    with open(state["template_path"], 'r', encoding='utf-8') as f:
        state["template_content"] = f.read()
    return {"documents": docs, "template_content": state["template_content"]}