from brd_gen_agent.state.SRSState import SRSState
from brd_gen_agent.utils.log import logged_node
import os
@logged_node
def save_output_node(state: SRSState, config=None) -> SRSState:
    output_dir = os.getcwd()
    file_name = f"{state['project_name']}.md"
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(state["final_srs"])
    print(f"SRS 已保存至：{output_path}")
    return {"status": "completed"}