# Prompts 目录

此目录用于存放各种 Agent 使用的提示词模板。

## 建议的文件结构

- `template_prompts/` - 模板代理的提示词
- `project_prompts/` - 项目代理的提示词
- `topic_prompts/` - 主题代理的提示词
- `planner_prompts/` - 规划代理的提示词
- `evidence_prompts/` - 证据代理的提示词
- `writer_prompts/` - 写作代理的提示词
- `reviewer_prompts/` - 评审代理的提示词

## 提示词文件格式

建议使用 `.txt` 或 `.json` 格式存储提示词模板，例如：

```txt
你是一个专业的软件需求分析师。请根据以下信息生成SRS文档的{section_name}章节。

项目信息：
{project_info}

相关证据：
{evidence}

要求：
1. 内容准确、完整
2. 符合SRS写作规范
3. 使用清晰的结构
```
