"""
主题图谱 - Topic Graph
建立项目主题知识库，替代传统向量库
用于存储和管理各主题相关的证据材料
"""

from typing import Dict, List
from graph.state import TopicNode, Evidence


class TopicGraph:
    """主题图谱管理类"""
    
    def __init__(self):
        # key为主题名（如"用户管理"），value为主题节点
        self.topics: Dict[str, TopicNode] = {}
    
    def add_topic(self, topic_name: str):
        """添加主题节点"""
        if topic_name not in self.topics:
            self.topics[topic_name] = TopicNode(name=topic_name)
    
    def add_evidence(self, topic_name: str, evidence: Evidence):
        """为主题添加证据"""
        if topic_name not in self.topics:
            self.add_topic(topic_name)
        
        self.topics[topic_name].evidences.append(evidence)
    
    def add_evidences(self, topic_name: str, evidences: List[Evidence]):
        """批量为主题添加证据"""
        for evidence in evidences:
            self.add_evidence(topic_name, evidence)
    
    def get_topic(self, topic_name: str) -> TopicNode:
        """获取主题节点"""
        return self.topics.get(topic_name)
    
    def get_evidences(self, topic_name: str) -> List[Evidence]:
        """获取主题的所有证据"""
        topic = self.topics.get(topic_name)
        if topic:
            return topic.evidences
        return []
    
    def get_all_topics(self) -> List[str]:
        """获取所有主题名称"""
        return list(self.topics.keys())
    
    def has_topic(self, topic_name: str) -> bool:
        """检查主题是否存在"""
        return topic_name in self.topics
    
    def to_dict(self) -> Dict[str, List[Dict]]:
        """转换为字典格式（用于序列化）"""
        result = {}
        for topic_name, topic_node in self.topics.items():
            result[topic_name] = [
                {
                    'source': e.source,
                    'section': e.section,
                    'content': e.content,
                    'relevance_score': e.relevance_score
                }
                for e in topic_node.evidences
            ]
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, List[Dict]]) -> 'TopicGraph':
        """从字典创建TopicGraph"""
        graph = cls()
        for topic_name, evidences_data in data.items():
            graph.add_topic(topic_name)
            for e_data in evidences_data:
                evidence = Evidence(
                    source=e_data['source'],
                    section=e_data.get('section', ''),
                    content=e_data['content'],
                    relevance_score=e_data.get('relevance_score', 0.0)
                )
                graph.add_evidence(topic_name, evidence)
        return graph
    
    def clear(self):
        """清空图谱"""
        self.topics.clear()
