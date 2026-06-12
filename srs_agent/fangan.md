# 软件需求规格说明书（SRS）自动生成 Agent 技术方案

## 1. 项目背景

### 1.1 项目目标

构建一个基于大语言模型（LLM）和 LangGraph 的软件需求规格说明书（SRS）自动生成 Agent。

系统能够读取项目目录中的各类需求资料，通过理解项目全量知识，自动按照指定的 SRS 模板生成完整的软件需求规格说明书。

### 1.2 核心目标

解决传统 RAG 方案在需求文档生成中的以下问题：

* 需求遗漏
* 检索不完整
* 跨文档关联能力弱
* 上下文长度限制
* 长文档生成质量下降

### 1.3 核心原则

Agent 不依赖传统「检索即生成」模式，而采用：

全量项目理解 → 项目知识抽取 → 主题知识构建 → 按章节生成

从而最大限度降低需求遗漏风险。

---

# 2. 总体架构设计

## 2.1 系统架构

```text
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

---

# 3. 技术选型

## 3.1 开发框架

| 组件      | 技术                |
| ------- | ----------------- |
| Agent编排 | LangGraph         |
| LLM调用   | LangChain         |
| 数据模型    | Pydantic          |
| 异步任务    | asyncio           |
| 配置管理    | pydantic-settings |

---

## 3.2 模型选择

### 主模型

```text
Qwen3-235B-A22B-Instruct
```

职责：

* 项目理解
* 知识提取
* 章节写作

优势：

* 中文能力强
* 长上下文能力优秀
* 需求分析能力优秀

---

### 审查模型

```text
DeepSeek-R1
```

职责：

* 一致性检查
* 需求覆盖检查
* 文档审查

---

## 3.3 文档解析

| 类型   | 技术            |
| ---- | ------------- |
| docx | python-docx   |
| pdf  | pymupdf       |
| pptx | python-pptx   |
| xlsx | pandas        |
| csv  | pandas        |
| md   | markdown      |
| html | BeautifulSoup |
| 图片   | Qwen-VL       |

---

# 4. 文件解析模块

## 4.1 支持格式

### 文档类

```text
docx
pdf
txt
md
html
rst
```

### 表格类

```text
xlsx
xls
csv
```

### 演示文稿

```text
pptx
ppt
```

### 图片

```text
png
jpg
jpeg
bmp
```

---

## 4.2 文件统一结构

所有文件转换为统一结构：

```json
{
  "file_name":"PRD.docx",
  "file_type":"docx",
  "content":"完整文本",
  "metadata":{
      "page_count":20
  }
}
```

---

# 5. 项目知识提取模块

## 5.1 目标

从所有文件中抽取项目知识。

避免依赖向量检索。

---

## 5.2 提取内容

### 功能模块

例如：

```json
[
  "用户管理",
  "订单管理",
  "支付管理"
]
```

---

### 用户角色

```json
[
  "管理员",
  "普通用户",
  "客服"
]
```

---

### 数据实体

```json
[
  "用户",
  "订单",
  "商品"
]
```

---

### 外部系统

```json
[
  "微信支付",
  "短信平台"
]
```

---

### 非功能需求

```json
[
  "高可用",
  "高并发",
  "安全审计"
]
```

---

# 6. Project Memory设计

## 6.1 数据结构

```json
{
  "project_name":"XX系统",

  "roles": [],

  "modules": [],

  "entities": [],

  "apis": [],

  "tables": [],

  "external_systems": [],

  "non_functional_requirements": []
}
```

---

## 6.2 作用

作为整个 Agent 的长期记忆。

所有章节共享。

避免章节之间产生矛盾。

---

# 7. Topic Graph设计

## 7.1 目标

建立项目主题知识库。

替代传统向量库。

---

## 7.2 示例

```json
{
  "用户管理":[
      Evidence1,
      Evidence2,
      Evidence3
  ],

  "订单管理":[
      Evidence4,
      Evidence5
  ]
}
```

---

## 7.3 Evidence结构

```json
{
  "source":"PRD.docx",

  "section":"用户管理",

  "content":"管理员可以新增用户"
}
```

---

# 8. 模板解析模块

## 8.1 输入

SRS模板：

```text
1 引言

2 总体描述

3 功能需求

3.1 用户管理

3.2 订单管理

4 接口需求
```

---

## 8.2 输出

```json
[
  {
      "id":"3.1",
      "title":"用户管理"
  },
  {
      "id":"3.2",
      "title":"订单管理"
  }
]
```

---

# 9. 章节规划模块

## 9.1 功能

分析章节需要哪些信息。

例如：

章节：

```text
3.1 用户管理
```

输出：

```json
{
  "required_topics":[
      "用户管理",
      "用户角色",
      "用户权限"
  ]
}
```

---

# 10. Evidence Builder

## 10.1 功能

从 Topic Graph 中提取章节证据。

---

## 10.2 输入

```json
{
  "section":"用户管理"
}
```

---

## 10.3 输出

```json
[
  {
      "source":"prd.docx",
      "content":"管理员新增用户"
  },

  {
      "source":"api.md",
      "content":"POST /users"
  },

  {
      "source":"会议纪要.docx",
      "content":"支持LDAP同步"
  }
]
```

---

# 11. Section Writer

## 11.1 输入

```json
{
  "section":"用户管理",

  "project_memory": {},

  "evidence":[]
}
```

---

## 11.2 Prompt原则

* 严格遵循SRS规范
* 不允许虚构
* 仅依据证据写作
* 使用REQ编号
* 输出Markdown

---

## 11.3 输出示例

```markdown
# 3.1 用户管理

## 功能描述

系统应支持用户管理功能。

### REQ-USER-001

管理员应能够新增用户。

### REQ-USER-002

管理员应能够修改用户信息。

### REQ-USER-003

系统应支持LDAP同步。
```

---

# 12. 一致性审查模块

## 12.1 检查项

### 术语一致性

检查：

```text
用户
客户
终端用户
```

是否混用。

---

### 功能覆盖率

检查：

模板要求的章节是否全部完成。

---

### 需求覆盖率

检查：

Project Memory中的需求是否全部被覆盖。

---

### 编号连续性

检查：

```text
REQ-001
REQ-002
REQ-004
```

发现缺失编号。

---

# 13. LangGraph工作流

```text
START

↓
Load Files

↓
Parse Documents

↓
Build Project Memory

↓
Build Topic Graph

↓
Parse Template

↓
Section Planner

↓
Evidence Builder

↓
Section Writer

↓
Update Memory

↓
Next Section ?

├─ Yes → Section Planner
└─ No

↓
Consistency Review

↓
Export Markdown

↓
END
```

---

# 14. 输出设计

## 第一阶段

输出：

```text
SRS.md
```

---

## 第二阶段

新增：

```text
SRS.docx
```

实现方式：

```text
Markdown
    ↓
Pandoc
    ↓
Word
```

---

# 15. 后续扩展

## V2

引入向量库

```text
Qdrant
Milvus
```

作为补充召回。

---

## V3

引入知识图谱

```text
Neo4j
```

构建：

* 角色关系
* 模块关系
* 接口关系

---

## V4

多Agent协作

```text
Planner Agent

Writer Agent

Review Agent

QA Agent
```

提升超大型项目生成能力。

---

# 16. 预期效果

对于一个包含：

* PRD
* 原型图
* API文档
* 数据库设计
* 会议纪要
* 测试用例

的项目目录。

Agent能够：

1. 自动理解项目全量知识
2. 自动构建项目知识模型
3. 自动分析SRS模板
4. 自动按章节生成内容
5. 自动检查一致性
6. 自动输出标准SRS文档

最终生成质量接近中高级需求分析师编写的软件需求规格说明书。
