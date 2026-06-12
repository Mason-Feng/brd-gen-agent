from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from brd_gen_agent.workflow import build_srs_workflow
from brd_gen_agent.state.SRSState import SRSState

import uvicorn

app = FastAPI()
workflow = build_srs_workflow()

class SRSRequest(BaseModel):
    folder_path: str = Field(..., description="业务文档文件夹的绝对路径")
    codebase_path: str = Field("", description="代码工程绝对路径（可选）")
    template_path: str = Field(..., description="需求规格说明书模板的绝对路径")
    project_name: str = Field("", description="输出文件名（不含扩展名），不填则从模板文件名衍生")

@app.post("/generate-srs")
def generate_srs(req: SRSRequest):
    initial_state: SRSState = {
        "folder_path": req.folder_path,
        "codebase_path": req.codebase_path or None,
        "template_path": req.template_path,
        "project_name": req.project_name,
        "documents": [],
        "context_text": "",
        "template_content": "",
        "template_sections": [],
        "outline": [],
        "sections_content": {},
        "current_section_idx": 0,
        "final_srs": "",
        "status": "running",
        "error_message": ""
    }
    try:
        final_state = workflow.invoke(initial_state)
        return {"status": "success", "file": f"{final_state['project_name']}.md"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)