import os
from langchain_openai import ChatOpenAI



# deepseek_llm = ChatOpenAI(
#     model_name="deepseek-v4-pro",
#     openai_api_key="sk-8198420a9ca146fa86438c4832ea0b65",
#     openai_api_base="https://api.deepseek.com/v1",
#     max_tokens=2000
# )

deepseek_llm = ChatOpenAI(
    model_name="qwen3.7-max",
    openai_api_key="sk-796a62beddc24e3abe2d5daf668d73b4",
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    max_tokens=2000
)