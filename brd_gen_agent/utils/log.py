import logging
import functools
import time
from brd_gen_agent.state.SRSState import SRSState

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# 节点装饰器，自动记录日志
def logged_node(func):
    @functools.wraps(func)
    def wrapper(state: SRSState, config=None):
        logger = setup_logger(func.__name__)
        logger.info(f"进入节点，当前状态摘要：{ {k: type(v).__name__ for k, v in state.items() if k not in ('documents', 'context_text', 'sections_content')} }")
        start = time.time()
        try:
            result = func(state, config)
            logger.info(f"节点执行成功，耗时 {time.time()-start:.2f}s，输出键：{result.keys()}")
            return result
        except Exception as e:
            logger.error(f"节点执行失败：{str(e)}", exc_info=True)
            raise
    return wrapper

@logged_node
def init_node(state: SRSState) -> SRSState:
    # 验证输入路径存在
    import os
    if not os.path.isdir(state["folder_path"]):
        raise ValueError(f"文件夹路径不存在：{state['folder_path']}")
    if state["codebase_path"] and not os.path.isdir(state["codebase_path"]):
        raise ValueError(f"代码工程路径不存在：{state['codebase_path']}")
    if not os.path.isfile(state["template_path"]):
        raise ValueError(f"模板文件不存在：{state['template_path']}")
    # 若未提供 project_name，从模板文件名提取
    if not state.get("project_name"):
        template_file = os.path.basename(state["template_path"])
        state["project_name"] = os.path.splitext(template_file)[0] + "_SRS"
    return {}