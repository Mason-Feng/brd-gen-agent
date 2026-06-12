# 快速开始指南

## 1. 环境准备

### 安装依赖

```bash
cd srs_agent
pip install -r requirements.txt
```

### 配置LLM（可选）

如果需要使用LLM功能，需要配置API密钥：

```python
import os

# OpenAI
os.environ["OPENAI_API_KEY"] = "your-api-key"

# 或阿里云Qwen
os.environ["DASHSCOPE_API_KEY"] = "your-api-key"
```

## 2. 准备输入文件

### 项目文档

将项目相关文档放在一个目录中，支持以下格式：
- PRD文档 (.docx, .pdf)
- API文档 (.md, .html)
- 数据库设计 (.xlsx, .sql)
- 会议纪要 (.docx, .txt)
- 原型图截图 (.png, .jpg)

示例目录结构：
```
my_project/
├── PRD.docx
├── API_Documentation.md
├── Database_Design.xlsx
├── Meeting_Notes.docx
└── screenshots/
    ├── page1.png
    └── page2.png
```

### SRS模板

准备一个SRS模板文件（Markdown格式），例如：

```markdown
# 1 引言

## 1.1 目的

## 1.2 范围

# 2 总体描述

## 2.1 用户特征

## 2.2 约束

# 3 功能需求

## 3.1 用户管理

## 3.2 订单管理

# 4 接口需求

## 4.1 用户界面

## 4.2 硬件接口

## 4.3 软件接口
```

## 3. 运行Agent

### 方法1: 使用main.py

```python
from srs_agent.main import main

result = main()
```

### 方法2: 手动创建工作流

```python
from graph.workflow import build_srs_workflow
from graph.state import SRSState

# 创建工作流
workflow = build_srs_workflow()

# 初始化状态
initial_state = SRSState(
    project_dir='/path/to/my_project',
    input_files=[
        '/path/to/my_project/PRD.docx',
        '/path/to/my_project/API_Documentation.md',
        '/path/to/my_project/Database_Design.xlsx',
    ],
    template_path='/path/to/srs_template.md',
    output_path='output/srs.md'
)

# 执行工作流
result = workflow.invoke(initial_state)

print(f"SRS生成完成: {result['output_path']}")
```

## 4. 查看输出

生成的SRS文档将保存在指定的输出路径（Markdown格式）。

```bash
cat output/srs.md
```

或使用Markdown编辑器查看。

## 5. 常见问题

### Q: 如何添加自定义解析器？

A: 在 `parsers/` 目录下创建新的解析器文件，实现统一接口，然后在 `parsers/document_parser.py` 中注册。

### Q: 如何调整生成的内容质量？

A: 
1. 完善提示词模板（在 `prompts/` 目录）
2. 调整LLM参数（temperature、max_tokens等）
3. 提供更多高质量的输入文档

### Q: 支持哪些语言？

A: 目前主要支持中文，通过配置不同的LLM模型也可以支持其他语言。

### Q: 如何处理大型项目？

A: 
1. 确保有足够的内存和存储空间
2. 考虑分批处理文档
3. 使用更强大的LLM模型

## 6. 下一步

- 阅读 [README.md](README.md) 了解完整架构
- 查看 [fangan.md](fangan.md) 了解技术方案
- 探索各个Agent的实现细节
- 根据项目需求定制开发

## 7. 获取帮助

如遇到问题：
1. 检查错误日志
2. 查看TODO列表了解已知限制
3. 提交Issue或联系开发团队
