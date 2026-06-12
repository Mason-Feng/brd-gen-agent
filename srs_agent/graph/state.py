"""
SRS Agent 状态定义
基于方案文档设计的数据结构
"""

from typing import TypedDict, List, Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ParsedDocument:
    """解析后的文档 - 统一文件结构"""
    file_name: str
    file_type: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Section:
    """SRS模板章节"""
    id: str  # 章节编号，如 "3.1"
    title: str
    level: int = 1  # 章节层级
    content: str = ""  # 生成的内容
    requirements: str = ""  # 章节要求/提示词（从模板中提取的描述文本）
    subsections: List['Section'] = field(default_factory=list)


@dataclass
class Evidence:
    """证据信息 - 支撑章节内容的原始材料"""
    source: str  # 来源文件名
    content: str  # 证据内容
    section: str = ""  # 原文档中的章节
    relevance_score: float = 0.0  # 相关性评分


@dataclass
class TopicNode:
    """主题节点 - Topic Graph的基本单元"""
    name: str  # 主题名称，如"用户管理"
    evidences: List[Evidence] = field(default_factory=list)


class SRSState(TypedDict):
    """SRS生成状态 - LangGraph工作流状态"""
    
    # ===== 阶段1: 文件加载与解析 =====
    # 输入的项目目录路径
    project_dir: str
    # 输入文件路径列表
    input_files: List[str]
    # 解析后的文档列表
    parsed_documents: List[ParsedDocument]
    
    # ===== 阶段2: 项目知识提取 =====
    # Project Memory - 项目全量知识
    project_memory: Dict[str, Any]  # 包含 project_name, roles, modules, entities, apis, tables, external_systems, non_functional_requirements
    
    # ===== 阶段3: 主题图谱构建 =====
    # Topic Graph - 主题知识库
    topic_graph: Dict[str, TopicNode]  # key为主题名，value为主题节点
    
    # ===== 阶段4: 模板解析 =====
    # SRS模板文件路径
    template_path: str
    # 解析后的模板结构
    template_sections: List[Section]
    
    # ===== 阶段5: 章节规划与生成 =====
    # 当前处理的章节索引
    current_section_index: int
    # 章节写作计划
    section_plan: Dict[str, Any]  # 包含 required_topics
    # 当前章节的证据集合
    current_evidences: List[Evidence]
    # 生成的章节内容 (key为章节id，如"3.1")
    sections_content: Dict[str, str]
    
    # ===== 阶段6: 一致性审查 =====
    # 评审意见
    review_comments: List[Dict[str, Any]]
    # 是否需要重新生成
    needs_revision: bool
    
    # ===== 输出 =====
    # 最终输出路径      
    output_path: str
    # 生成的Markdown内容
    final_markdown: str
    
    # ===== 错误处理 =====
    # 错误信息
    errors: List[str]
