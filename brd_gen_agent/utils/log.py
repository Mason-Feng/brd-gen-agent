import logging
import functools
import os
import time
from pathlib import Path
from brd_gen_agent.state.SRSState import SRSState

LOG_FILE = os.environ.get(
    "BRD_GEN_AGENT_LOG_FILE",
    str(Path(__file__).resolve().parents[2] / "logs" / "brd-gen-agent.log")
)

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def setup_logger(name: str):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

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

