# 📝 SRS Agent 日志功能 - 快速参考

## 🚀 快速开始

### 1. 为节点添加日志（一行代码）

```python
from utils.logger import log_node_execution

@log_node_execution
def my_agent_node(state: SRSState) -> SRSState:
    return state
```

### 2. 手动记录日志

```python
from utils.logger import log_info, log_error

log_info("这是一条信息")
log_error("这是错误", exc=exception)
```

### 3. 工作流日志

```python
from utils.logger import log_workflow_start, log_workflow_end

log_workflow_start("My Workflow")
# ... 执行工作流 ...
log_workflow_end(success=True, total_duration=120.5)
```

---

## 📊 日志输出示例

### 正常执行
```
10:50:25 - INFO - ▶️  开始执行节点: template_agent_node
10:50:25 - INFO - 📥 输入状态: {"template_path": "str(45 chars)"}
10:50:26 - INFO - ✅ 节点执行成功 | 耗时: 0.856s
```

### 错误情况
```
10:50:25 - ERROR - ❌ 节点执行失败 | 耗时: 0.001s
10:50:25 - ERROR -    错误类型: ValueError
10:50:25 - ERROR -    错误信息: 没有可分析的文档
```

### 工作流
```
🚀🚀🚀 工作流启动: SRS Generation Workflow
✨✨✨ 工作流执行成功! 总耗时: 12.345s
```

---

## 🔧 配置

### 环境变量
```bash
export SRS_AGENT_LOG_DIR="/path/to/logs"
export SRS_AGENT_LOG_FILE="/path/to/srs-agent.log"
```

### 日志级别
```python
import logging
logger = setup_logger("srs_agent", level=logging.DEBUG)
```

---

## 📁 文件位置

- **日志文件：** `logs/srs-agent.log`
- **使用指南：** `utils/LOGGING_GUIDE.md`
- **测试脚本：** `tests/test_logging.py`

---

## 💡 提示

- ✅ 所有 Agent 节点已自动添加日志装饰器
- ✅ 日志同时输出到控制台和文件
- ✅ 自动记录状态变化和耗时
- ✅ 错误会自动记录堆栈跟踪

---

**详细文档：** 参见 [utils/LOGGING_GUIDE.md](utils/LOGGING_GUIDE.md)
