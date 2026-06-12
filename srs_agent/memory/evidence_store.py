"""
证据存储 - Evidence Store
管理和检索证据信息，支持按来源、主题等维度组织证据
"""

from typing import Dict, List, Optional
from graph.state import Evidence


class EvidenceStore:
    """证据存储管理类"""
    
    def __init__(self):
        # 所有证据的列表
        self.evidences: List[Evidence] = []
        # 按来源文件索引: source -> [evidence]
        self.source_index: Dict[str, List[Evidence]] = {}
    
    def add_evidence(self, evidence: Evidence):
        """添加证据"""
        self.evidences.append(evidence)
        
        # 建立来源索引
        if evidence.source not in self.source_index:
            self.source_index[evidence.source] = []
        self.source_index[evidence.source].append(evidence)
    
    def add_evidences(self, evidences: List[Evidence]):
        """批量添加证据"""
        for evidence in evidences:
            self.add_evidence(evidence)
    
    def get_evidences_by_source(self, source: str) -> List[Evidence]:
        """根据来源文件获取证据列表"""
        return self.source_index.get(source, [])
    
    def get_all_evidences(self) -> List[Evidence]:
        """获取所有证据"""
        return self.evidences
    
    def search_evidences(self, keyword: str) -> List[Evidence]:
        """搜索证据（简单关键词匹配）"""
        results = []
        for evidence in self.evidences:
            if keyword.lower() in evidence.content.lower() or \
               keyword.lower() in evidence.source.lower():
                results.append(evidence)
        return results
    
    def get_sources(self) -> List[str]:
        """获取所有来源文件列表"""
        return list(self.source_index.keys())
    
    def count(self) -> int:
        """获取证据总数"""
        return len(self.evidences)
    
    def clear(self):
        """清空所有证据"""
        self.evidences.clear()
        self.source_index.clear()
