"""
SRS Agent 工作流定义
"""

from langgraph.graph import StateGraph, END
from graph.state import SRSState
from agents.template_agent import template_agent_node
from agents.project_agent import project_agent_node
from agents.topic_agent import topic_agent_node
from agents.planner_agent import planner_agent_node
from agents.evidence_agent import evidence_agent_node
from agents.writer_agent import writer_agent_node
from agents.reviewer_agent import reviewer_agent_node
from exporters.markdown_exporter import export_to_markdown


def build_srs_workflow():
    """构建SRS生成工作流"""
    
    workflow = StateGraph(SRSState)
    
    # 添加节点
    workflow.add_node("template_agent", template_agent_node)
    workflow.add_node("project_agent", project_agent_node)
    workflow.add_node("topic_agent", topic_agent_node)
    workflow.add_node("planner_agent", planner_agent_node)
    workflow.add_node("evidence_agent", evidence_agent_node)
    workflow.add_node("writer_agent", writer_agent_node)
    workflow.add_node("reviewer_agent", reviewer_agent_node)
    workflow.add_node("exporter", export_to_markdown)
    
    # 定义工作流边
    workflow.set_entry_point("template_agent")
    workflow.add_edge("template_agent", "project_agent")
    workflow.add_edge("project_agent", "topic_agent")
    workflow.add_edge("topic_agent", "planner_agent")
    workflow.add_edge("planner_agent", "evidence_agent")
    workflow.add_edge("evidence_agent", "writer_agent")
    workflow.add_edge("writer_agent", "reviewer_agent")
    workflow.add_edge("reviewer_agent", "exporter")
    workflow.add_edge("exporter", END)
    
    return workflow.compile()
