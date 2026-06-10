
from langgraph.graph import StateGraph,END

from brd_gen_agent.state.SRSState import SRSState

from brd_gen_agent.node.init_node import init_node
from brd_gen_agent.node.parse_files_node import parse_files_node
from brd_gen_agent.node.build_context_node import build_context_node
from brd_gen_agent.node.generate_outline_node import generate_outline_node
from brd_gen_agent.node.write_section_node import write_section_node, should_continue_sections
from brd_gen_agent.node.assemble_document_node import assemble_document_node
from brd_gen_agent.node.save_output_node import save_output_node

def build_srs_workflow():
    workflow = StateGraph(SRSState)

    workflow.add_node("init", init_node)
    workflow.add_node("parse_files", parse_files_node)
    workflow.add_node("build_context", build_context_node)
    workflow.add_node("generate_outline", generate_outline_node)
    workflow.add_node("write_section", write_section_node)
    workflow.add_node("assemble_document", assemble_document_node)
    workflow.add_node("save_output", save_output_node)

    workflow.set_entry_point("init")
    workflow.add_edge("init", "parse_files")
    workflow.add_edge("parse_files", "build_context")
    workflow.add_edge("build_context", "generate_outline")
    # 大纲生成后进入逐节生成循环
    workflow.add_edge("generate_outline", "write_section")
    workflow.add_conditional_edges(
        "write_section",
        should_continue_sections,
        {"write_section": "write_section", "assemble_document": "assemble_document"}
    )
    workflow.add_edge("assemble_document", "save_output")
    workflow.add_edge("save_output", END)

    return workflow.compile()