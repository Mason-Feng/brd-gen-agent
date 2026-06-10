
from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node



@logged_node
def init_node(state: SRSState, config=None) -> SRSState:
    # 验证输入路径存在
    import os
    if not os.path.isdir(state["folder_path"]):
        raise ValueError(f"文件夹路径不存在：{state['folder_path']}")
    if state["codebase_path"] and not os.path.isdir(state["codebase_path"]):
        raise ValueError(f"代码工程路径不存在：{state['codebase_path']}")
    if not os.path.isfile(state["template_path"]):
        raise ValueError(f"模板文件不存在：{state['template_path']}")
    # 若未提供 project_name，从模板文件名提取
    if not state.get("project_name"):
        template_file = os.path.basename(state["template_path"])
        state["project_name"] = os.path.splitext(template_file)[0] + "_SRS"
    return {}