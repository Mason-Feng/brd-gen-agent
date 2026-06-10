import os
import sys
from pydantic import BaseModel, Field

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from brd_gen_agent.workflow.build_srs_workflow import build_srs_workflow
from brd_gen_agent.state.SRSState import SRSState

if __name__ == "__main__":
    folder_path = "D:\\project\\brd-gen-agent\\测试文件\\受益人业务相关文档"
    codebase_path = ""  
    template_path = "D:\\project\\brd-gen-agent\\测试文件\\业务需求规格说明书模板.md"
    project_name = "受益所有人信息查询管理系统接入"
    initial_state: SRSState = {
        "folder_path": folder_path,
        "codebase_path": codebase_path or None,
        "template_path": template_path,
        "project_name": project_name,
        "documents": [],
        "context_text": "",
        "template_content": "",
        "outline": [],
        "sections_content": {},
        "current_section_idx": 0,
        "final_srs": "",
        "status": "running",
        "error_message": ""
    }
    workflow = build_srs_workflow()
    final_state = workflow.invoke(initial_state)
    print({"status": "success", "file": f"{final_state['project_name']}.md"})