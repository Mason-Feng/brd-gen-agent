import os
from pathlib import Path
from typing import List, Dict, Optional
from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node, setup_logger

logger = setup_logger(__name__)

def parse_all_files(root_dir: str) -> List[Dict[str, str]]:
    """递归提取所有可识别的文本文件"""
    logger.info(f"开始解析目录: {root_dir}")
    documents = []
    file_count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            # 跳过 Word 的临时文件（例如以 '~$' 开头的临时文件）
            if fname.startswith('~$'):
                logger.debug(f"跳过临时文件: {fname}")
                continue
            file_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(file_path, root_dir)
            logger.debug(f"处理文件: {rel_path}")
            text = extract_text(file_path)
            if text is not None:
                documents.append({"path": rel_path, "content": text})
                file_count += 1
                logger.info(f"✓ 成功提取: {rel_path} ({len(text)} 字符)")
            else:
                logger.debug(f"✗ 跳过文件: {rel_path} (不支持的格式)")
    logger.info(f"目录解析完成: {root_dir} - 共提取 {file_count} 个文件")
    return documents

def extract_text(file_path: str) -> Optional[str]:
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in ['.md', '.txt', '.py', '.java', '.js', '.ts', '.html', '.css', '.c', '.cpp', '.h', '.yaml', '.yml', '.json']:
            logger.debug(f"读取文本文件: {ext}")
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            logger.debug(f"使用 PyPDF2 提取 PDF 内容")
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            logger.debug(f"PDF 提取完成: {len(reader.pages)} 页")
            return text
        elif ext == '.docx':
            logger.debug(f"使用 python-docx 提取 Word 内容")
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            logger.debug(f"Word 提取完成: {len(doc.paragraphs)} 段落")
            return text
        else:
            logger.debug(f"不支持的文件类型: {ext}")
            return None
    except Exception as e:
        logger.warning(f"文件解析失败: {file_path} - 错误: {str(e)}")
        return None

@logged_node
def parse_files_node(state: SRSState, config=None) -> SRSState:
    logger.info("=" * 50)
    logger.info("开始文件解析节点")
    
    logger.info(f"解析业务文档目录: {state['folder_path']}")
    docs = parse_all_files(state["folder_path"])
    logger.info(f"业务文档解析完成，共 {len(docs)} 个文件")
    
    if state.get("codebase_path"):
        logger.info(f"解析代码库目录: {state['codebase_path']}")
        codebase_docs = parse_all_files(state["codebase_path"])
        docs.extend(codebase_docs)
        logger.info(f"代码库解析完成，共 {len(codebase_docs)} 个文件，总计 {len(docs)} 个文件")
    else:
        logger.info("跳过代码库解析 (未提供路径)")
    
    logger.info(f"读取模板文件: {state['template_path']}")
    with open(state["template_path"], 'r', encoding='utf-8') as f:
        state["template_content"] = f.read()
    logger.info(f"模板读取完成 ({len(state['template_content'])} 字符)")
    
    logger.info("文件解析节点完成")
    logger.info("=" * 50)
    return {"documents": docs, "template_content": state["template_content"]}