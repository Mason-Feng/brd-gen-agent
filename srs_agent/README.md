# SRS Agent - 软件需求规格说明书自动生成系统

基于大语言模型（LLM）和 LangGraph 的智能 SRS 文档生成 Agent，能够读取项目目录中的各类需求资料，通过理解项目全量知识，自动按照指定的 SRS 模板生成完整的软件需求规格说明书。

## 🎯 核心目标

解决传统 RAG 方案在需求文档生成中的问题：
- ✅ 需求遗漏
- ✅ 检索不完整
- ✅ 跨文档关联能力弱
- ✅ 上下文长度限制
- ✅ 长文档生成质量下降

## 💡 核心原则

Agent 不依赖「检索即生成」模式，而采用：

```
全量项目理解 → 项目知识抽取 → 主题知识构建 → 按章节生成
```

从而最大限度降低需求遗漏风险。

---

## 📁 目录结构

```
srs_agent/
├── main.py                      # 主入口文件
├── graph/                       # 工作流和状态定义
│   ├── workflow.py             # LangGraph 工作流定义
│   └── state.py                # 状态数据结构定义
├── parsers/                     # 文档解析器
│   ├── docx_parser.py          # Word 文档解析
│   ├── pdf_parser.py           # PDF 文档解析
│   ├── excel_parser.py         # Excel 表格解析
│   ├── ppt_parser.py           # PowerPoint 演示文稿解析
│   ├── markdown_parser.py      # Markdown 文档解析
│   ├── html_parser.py          # HTML 网页解析
│   └── image_parser.py         # 图像 OCR 解析
├── agents/                      # 智能代理
│   ├── template_agent.py       # 模板选择代理
│   ├── project_agent.py        # 项目信息提取代理
│   ├── topic_agent.py          # 主题分析代理
│   ├── planner_agent.py        # 写作规划代理
│   ├── evidence_agent.py       # 证据收集代理
│   ├── writer_agent.py         # 内容写作代理
│   └── reviewer_agent.py       # 文档评审代理
├── memory/                      # 记忆管理
│   ├── project_memory.py       # 项目记忆存储
│   ├── topic_graph.py          # 主题关系图谱
│   └── evidence_store.py       # 证据信息管理
├── exporters/                   # 导出器
│   └── markdown_exporter.py    # Markdown 格式导出
└── prompts/                     # 提示词模板
    └── README.md               # 提示词使用说明
```

## 📊 系统架构

```
Project Files
      │
      ▼
Document Parser
      │
      ▼
Knowledge Extractor
      │
      ▼
Project Memory
      │
      ▼
Topic Graph Builder
      │
      ▼
Template Analyzer
      │
      ▼
Section Planner
      │
      ▼
Evidence Builder
      │
      ▼
Section Writer
      │
      ▼
Consistency Reviewer
      │
      ▼
Markdown Exporter
```

## 📝 日志功能

SRS Agent 集成了详细的日志记录系统，可以追踪每个节点的执行情况。

### 功能特性

- ✅ **自动节点日志** - 使用 `@log_node_execution` 装饰器
- ✅ **状态追踪** - 记录输入/输出状态和变化
- ✅ **性能监控** - 记录每个节点的执行耗时
- ✅ **错误追踪** - 详细的错误信息和堆栈跟踪
- ✅ **工作流日志** - 记录整体执行情况

### 使用示例

```python
from utils.logger import log_node_execution

@log_node_execution
def my_agent_node(state: SRSState) -> SRSState:
    # 自动记录执行日志
    return state
```

### 日志输出示例

```
14:30:25 - INFO - ▶️  开始执行节点: template_agent_node
14:30:25 - INFO - 📥 输入状态: {"template_path": "str(45 chars)"}
14:30:26 - INFO - ✅ 节点执行成功 | 耗时: 0.856s
```

详细使用说明请参考：[utils/LOGGING_GUIDE.md](utils/LOGGING_GUIDE.md)

## 🔄 工作流程

```
START
  ↓
Load Files (加载项目文件)
  ↓
Parse Documents (解析文档)
  ↓
Build Project Memory (构建项目记忆)
  ↓
Build Topic Graph (构建主题图谱)
  ↓
Parse Template (解析SRS模板)
  ↓
Section Planner (章节规划)
  ↓
Evidence Builder (证据收集)
  ↓
Section Writer (章节写作)
  ↓
Update Memory (更新记忆)
  ↓
Next Section? ──Yes──→ Section Planner
  │
  No
  ↓
Consistency Review (一致性审查)
  ↓
Export Markdown (导出Markdown)
  ↓
END
```

### 工作流说明

1. **Template Agent** - 解析SRS模板，提取章节结构
2. **Project Agent** - 从输入文档中提取项目全量知识（角色、模块、实体、API等）
3. **Topic Agent** - 构建主题图谱，建立主题与证据的关联
4. **Planner Agent** - 分析每个章节需要的信息和主题
5. **Evidence Agent** - 从Topic Graph中提取章节相关证据
6. **Writer Agent** - 根据Project Memory和证据生成章节内容
7. **Reviewer Agent** - 检查术语一致性、功能覆盖率、需求覆盖率、编号连续性
8. **Exporter** - 将最终文档导出为Markdown格式

## 📝 支持的输入格式

### 文档类
- Microsoft Word (.docx)
- PDF (.pdf) - 使用 PyMuPDF
- Markdown (.md)
- HTML (.html, .htm)
- 文本文件 (.txt)

### 表格类
- Excel (.xlsx, .xls)
- CSV (.csv)

### 演示文稿
- PowerPoint (.pptx, .ppt)

### 图片
- PNG, JPG, JPEG, BMP - 使用 OCR (Qwen-VL)

## 🛠️ 技术栈

### 开发框架
| 组件 | 技术 |
|------|------|
| Agent编排 | LangGraph |
| LLM调用 | LangChain |
| 数据模型 | Pydantic |
| 异步任务 | asyncio |
| 配置管理 | pydantic-settings |

### 模型选择

**主模型**: Qwen3-235B-A22B-Instruct
- 职责：项目理解、知识提取、章节写作
- 优势：中文能力强、长上下文能力优秀、需求分析能力优秀

**审查模型**: DeepSeek-R1
- 职责：一致性检查、需求覆盖检查、文档审查

### 文档解析
| 类型 | 技术 |
|------|------|
| docx | python-docx |
| pdf | pymupdf (fitz) |
| pptx | python-pptx |
| xlsx/csv | pandas |
| md | markdown |
| html | BeautifulSoup |
| 图片 | Qwen-VL / pytesseract |

## 🚀 使用方法

### 基本用法

```python
from srs_agent.main import main

# 运行 SRS 生成工作流
result = main()
```

### 高级用法

```python
from graph.workflow import build_srs_workflow
from graph.state import SRSState

# 创建工作流
workflow = build_srs_workflow()

# 初始化状态
initial_state = SRSState(
    project_dir='/path/to/project',
    input_files=['file1.docx', 'file2.pdf'],
    template_path='/path/to/template.md',
    output_path='output/srs.md'
)

# 执行工作流
result = workflow.invoke(initial_state)
```

## 📦 依赖项

需要安装以下 Python 包：

### 核心框架
- langgraph>=0.0.50
- langchain>=0.1.0
- pydantic>=2.0.0

### 文档解析
- python-docx>=0.8.11
- pymupdf>=1.23.0 (fitz)
- pandas>=1.5.0
- openpyxl>=3.0.0
- python-pptx>=0.6.21
- beautifulsoup4>=4.12.0
- lxml>=4.9.0

### 图像处理和 OCR
- Pillow>=9.0.0
- pytesseract>=0.3.10

### LLM 集成（可选）
- openai>=1.0.0
- anthropic>=0.7.0

### 工具库
- typing-extensions>=4.5.0

安装命令：
```bash
pip install -r requirements.txt
```

## 🔧 扩展开发

### 添加新的解析器

在 `parsers/` 目录下创建新的解析器文件，实现统一的解析接口：

```python
def parse_xxx(file_path: str) -> Dict[str, Any]:
    """
    解析XXX格式文件
    
    Returns:
        {
            'content': '提取的文本内容',
            'metadata': {...},  # 可选元数据
            'success': True,
            'error': ''  # 仅在失败时提供
        }
    """
    try:
        # 解析逻辑
        return {
            'content': content,
            'metadata': {},
            'success': True
        }
    except Exception as e:
        return {
            'content': '',
            'metadata': {},
            'success': False,
            'error': str(e)
        }
```

然后在 `parsers/document_parser.py` 中注册该解析器。

### 添加新的 Agent

在 `agents/` 目录下创建新的 Agent 文件，实现节点函数：

```python
from graph.state import SRSState

def xxx_agent_node(state: SRSState) -> SRSState:
    """
    XXX Agent 节点
    
    功能：
    1. ...
    2. ...
    """
    print("[XXX Agent] 开始处理...")
    
    try:
        # 实现 Agent 逻辑
        # 从 state 中获取所需数据
        # 处理后将结果写入 state
        
        state['xxx_result'] = result
        
    except Exception as e:
        print(f"[XXX Agent] 错误: {str(e)}")
        if 'errors' not in state:
            state['errors'] = []
        state['errors'].append(str(e))
    
    return state
```

然后在 `graph/workflow.py` 中注册该节点并添加到工作流中。

## 📋 TODO

### 短期目标
- [ ] 实现各个 Agent 的 LLM 调用逻辑
- [ ] 集成 Qwen3-235B 和 DeepSeek-R1 模型
- [ ] 完善提示词模板（prompts目录）
- [ ] 实现真正的知识提取逻辑（而非简单规则匹配）
- [ ] 实现章节内容生成逻辑
- [ ] 实现一致性审查逻辑

### 中期目标
- [ ] 添加更多导出格式（Word、PDF等）
- [ ] 实现记忆持久化（保存到文件/数据库）
- [ ] 添加单元测试
- [ ] 完善错误处理和日志记录
- [ ] 支持增量更新（基于已有SRS进行修改）

### 长期目标 (V2-V4)
- [ ] V2: 引入向量库（Qdrant/Milvus）作为补充召回
- [ ] V3: 引入知识图谱（Neo4j）构建角色/模块/接口关系
- [ ] V4: 多Agent协作提升超大型项目生成能力

## ✨ 预期效果

对于一个包含以下资料的项目：
- PRD文档
- 原型图
- API文档
- 数据库设计
- 会议纪要
- 测试用例

Agent能够：

1. ✅ 自动理解项目全量知识
2. ✅ 自动构建项目知识模型
3. ✅ 自动分析SRS模板
4. ✅ 自动按章节生成内容
5. ✅ 自动检查一致性
6. ✅ 自动输出标准SRS文档

最终生成质量接近中高级需求分析师编写的软件需求规格说明书。

## 📄 许可证

MIT License
