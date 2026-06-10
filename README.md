# brd-gen-agent
Business Requirements Document，业务需求规格说明书生成agent

## 工作流架构

```mermaid
graph TD
    A[init<br/>初始化] --> B[parse_files<br/>解析文件]
    B --> C[build_context<br/>构建上下文]
    C --> D[generate_outline<br/>生成大纲]
    D --> E[write_section<br/>逐节写入]
    E -->|继续循环| E
    E -->|完成| F[assemble_document<br/>组装文档]
    F --> G[save_output<br/>保存输出]
    G --> H[END<br/>结束]
```

## 工作流说明

- **init**: 初始化工作流状态
- **parse_files**: 递归解析输入目录中的文档文件（支持 PDF、DOCX、TXT 等格式）
- **build_context**: 基于解析的文件内容构建上下文
- **generate_outline**: 使用 LLM 生成需求规格说明书的详细大纲
- **write_section**: 逐节生成文档内容，支持循环生成多个章节
- **assemble_document**: 将所有章节组装成完整文档
- **save_output**: 保存生成的文档到指定位置
