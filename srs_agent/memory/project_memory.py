"""
项目记忆 - Project Memory
存储和管理项目全量知识，作为整个Agent的长期记忆
所有章节共享，避免章节之间产生矛盾
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class ProjectMemoryData:
    """Project Memory 数据结构"""
    project_name: str = ""  # 项目名称
    roles: List[str] = field(default_factory=list)  # 用户角色
    modules: List[str] = field(default_factory=list)  # 功能模块
    entities: List[str] = field(default_factory=list)  # 数据实体
    apis: List[Dict[str, Any]] = field(default_factory=list)  # API接口
    tables: List[Dict[str, Any]] = field(default_factory=list)  # 数据库表
    external_systems: List[str] = field(default_factory=list)  # 外部系统
    non_functional_requirements: List[str] = field(default_factory=list)  # 非功能需求


class ProjectMemory:
    """项目记忆管理类"""
    
    def __init__(self):
        self.data = ProjectMemoryData()
    
    def set_project_name(self, name: str):
        """设置项目名称"""
        self.data.project_name = name
    
    def add_role(self, role: str):
        """添加用户角色"""
        if role not in self.data.roles:
            self.data.roles.append(role)
    
    def add_roles(self, roles: List[str]):
        """批量添加用户角色"""
        for role in roles:
            self.add_role(role)
    
    def add_module(self, module: str):
        """添加功能模块"""
        if module not in self.data.modules:
            self.data.modules.append(module)
    
    def add_modules(self, modules: List[str]):
        """批量添加功能模块"""
        for module in modules:
            self.add_module(module)
    
    def add_entity(self, entity: str):
        """添加数据实体"""
        if entity not in self.data.entities:
            self.data.entities.append(entity)
    
    def add_entities(self, entities: List[str]):
        """批量添加数据实体"""
        for entity in entities:
            self.add_entity(entity)
    
    def add_api(self, api: Dict[str, Any]):
        """添加API接口"""
        self.data.apis.append(api)
    
    def add_apis(self, apis: List[Dict[str, Any]]):
        """批量添加API接口"""
        self.data.apis.extend(apis)
    
    def add_table(self, table: Dict[str, Any]):
        """添加数据库表"""
        self.data.tables.append(table)
    
    def add_tables(self, tables: List[Dict[str, Any]]):
        """批量添加数据库表"""
        self.data.tables.extend(tables)
    
    def add_external_system(self, system: str):
        """添加外部系统"""
        if system not in self.data.external_systems:
            self.data.external_systems.append(system)
    
    def add_external_systems(self, systems: List[str]):
        """批量添加外部系统"""
        for system in systems:
            self.add_external_system(system)
    
    def add_non_functional_requirement(self, requirement: str):
        """添加非功能需求"""
        if requirement not in self.data.non_functional_requirements:
            self.data.non_functional_requirements.append(requirement)
    
    def add_non_functional_requirements(self, requirements: List[str]):
        """批量添加非功能需求"""
        for requirement in requirements:
            self.add_non_functional_requirement(requirement)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'project_name': self.data.project_name,
            'roles': self.data.roles,
            'modules': self.data.modules,
            'entities': self.data.entities,
            'apis': self.data.apis,
            'tables': self.data.tables,
            'external_systems': self.data.external_systems,
            'non_functional_requirements': self.data.non_functional_requirements
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectMemory':
        """从字典创建ProjectMemory"""
        memory = cls()
        memory.data = ProjectMemoryData(**data)
        return memory
    
    def clear(self):
        """清空所有记忆"""
        self.data = ProjectMemoryData()
