# SRS Agent 日志系统使用指南

## 📋 概述

SRS Agent 集成了详细的日志记录系统，可以追踪和记录每个节点的执行情况，包括：
- ✅ 节点输入/输出状态
- ✅ 执行耗时
- ✅ 状态变化
- ✅ 错误信息和堆栈跟踪
- ✅ 工作流整体执行情况

## 🎯 功能特性

### 1. 自动节点日志装饰器

使用 `@log_node_execution` 装饰器自动记录：

```python
from utils.logger import log_node_execution

@log_node_execution
def my_agent_node(state: SRSState) -> SRSState:
    # 你的代码
    return state
```

**自动记录内容：**
- ▶️ 节点开始执行时间
- 📥 输入状态摘要（类型和数量）
- 📌 关键输入数据（文件列表、路径等）
- 📤 输出状态摘要
- 🔄 状态变化（新增/修改的字段）
- ✅ 执行成功 + 耗时
- ❌ 执行失败 + 错误详情 + 堆栈跟踪

### 2. 工作流级别日志

```python
from utils.logger import log_workflow_start, log_workflow_end

# 工作流开始
log_workflow_start("SRS Generation Workflow")

# 工作流结束
log_workflow_end(success=True, total_duration=120.5)
```

### 3. 手动日志记录

```python
from utils.logger import log_debug, log_info, log_warning, log_error

log_debug("调试信息")
log_info("普通信息")
log_warning("警告信息")
log_error("错误信息", exc=some_exception)
```

## 📊 日志输出示例

### 控制台输出（简洁格式）

```
14:30:25 - INFO - ================================================================================
14:30:25 - INFO - ▶️  开始执行节点: template_agent_node
14:30:25 - INFO -    时间: 2026-06-12 14:30:25.123
14:30:25 - INFO - --------------------------------------------------------------------------------
14:30:25 - INFO - 📥 输入状态:
14:30:25 - INFO -    {
       "template_path": "str(45 chars)",
       "input_files": "list(3 items)"
     }
14:30:25 - INFO -    📌 模板路径: /path/to/template.md
14:30:25 - INFO - --------------------------------------------------------------------------------
14:30:26 - INFO - 📤 输出状态:
14:30:26 - INFO -    {
       "template_sections": "list(10 items)",
       "current_section_index": "int"
     }
14:30:26 - INFO - 🔄 状态变化:
14:30:26 - INFO -    新增 [template_sections]: list(10 items)
14:30:26 - INFO -    新增 [current_section_index]: int
14:30:26 - INFO - ✅ 节点执行成功 | 耗时: 0.856s
14:30:26 - INFO - ================================================================================
```

### 日志文件输出（详细格式）

```
2026-06-12 14:30:25 - srs_agent.template_agent_node - INFO - [template_agent.py:25] - ================================================================================
2026-06-12 14:30:25 - srs_agent.template_agent_node - INFO - [template_agent.py:26] - ▶️  开始执行节点: template_agent_node
2026-06-12 14:30:25 - srs_agent.template_agent_node - INFO - [template_agent.py:27] -    时间: 2026-06-12 14:30:25.123
...
```

## 🔧 配置选项

### 环境变量

```bash
# 日志目录（默认：项目根目录/logs）
export SRS_AGENT_LOG_DIR="/path/to/logs"

# 日志文件路径（默认：{LOG_DIR}/srs-agent.log）
export SRS_AGENT_LOG_FILE="/path/to/srs-agent.log"
```

### 日志级别

在代码中设置：

```python
import logging
from utils.logger import setup_logger

# 设置为 DEBUG 级别
logger = setup_logger("srs_agent", level=logging.DEBUG)

# 设置为 WARNING 级别
logger = setup_logger("srs_agent", level=logging.WARNING)
```

## 📁 日志文件位置

默认日志文件位置：
```
brd-gen-agent/
└── logs/
    └── srs-agent.log
```

## 💡 最佳实践

### 1. 为所有 Agent 节点添加装饰器

```python
from utils.logger import log_node_execution

@log_node_execution
def template_agent_node(state: SRSState) -> SRSState:
    ...

@log_node_execution
def project_agent_node(state: SRSState) -> SRSState:
    ...
```

### 2. 在关键步骤添加日志

```python
from utils.logger import log_info

def some_function():
    log_info("开始处理文档...")
    # 处理逻辑
    log_info(f"处理完成，共 {count} 个文档")
```

### 3. 错误处理

```python
from utils.logger import log_error

try:
    result = do_something()
except Exception as e:
    log_error(f"操作失败: {str(e)}", exc=e)
    raise
```

### 4. 性能监控

装饰器自动记录每个节点的执行时间，可以在日志中看到：
```
✅ 节点执行成功 | 耗时: 2.345s
```

## 🔍 日志分析

### 查看节点执行顺序

```bash
grep "▶️  开始执行节点" logs/srs-agent.log
```

### 查看执行失败的节点

```bash
grep "❌ 节点执行失败" logs/srs-agent.log
```

### 查看各节点耗时

```bash
grep "✅ 节点执行成功" logs/srs-agent.log
```

### 查看工作流执行情况

```bash
grep "工作流" logs/srs-agent.log
```

## 🚀 高级用法

### 自定义日志格式化器

```python
from utils.logger import setup_logger
import logging

logger = setup_logger("custom")

# 添加自定义处理器
custom_handler = logging.FileHandler("custom.log")
custom_format = logging.Formatter("[%(levelname)s] %(message)s")
custom_handler.setFormatter(custom_format)
logger.addHandler(custom_handler)
```

### 按模块分离日志

```python
# 为不同模块创建独立的 logger
parser_logger = setup_logger("srs_agent.parsers")
agent_logger = setup_logger("srs_agent.agents")
memory_logger = setup_logger("srs_agent.memory")
```

## 📝 注意事项

1. **不要移除装饰器**：确保所有 Agent 节点都有 `@log_node_execution` 装饰器
2. **异常处理**：装饰器会捕获并记录异常，然后重新抛出
3. **性能影响**：日志记录会有轻微性能开销，生产环境可调整日志级别
4. **日志轮转**：当前未实现日志轮转，大项目建议添加

## 🛠️ 故障排查

### 问题：看不到日志输出

**解决：**
1. 检查日志级别设置
2. 确认日志目录有写入权限
3. 检查环境变量配置

### 问题：日志文件过大

**解决：**
1. 提高日志级别（WARNING 或 ERROR）
2. 实现日志轮转（使用 `logging.handlers.RotatingFileHandler`）

### 问题：装饰器不生效

**解决：**
1. 确认正确导入：`from utils.logger import log_node_execution`
2. 确认装饰器在函数定义上方
3. 检查函数签名是否正确

## 📖 相关文档

- [README.md](../README.md) - 项目总体说明
- [fangan.md](../fangan.md) - 技术方案
- [QUICKSTART.md](../QUICKSTART.md) - 快速开始指南

---

**更新日期：** 2026-06-12  
**版本：** v1.0.0
