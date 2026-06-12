"""
SRS Agent 日志模块
提供详细的节点执行日志记录功能
"""

import logging
import functools
import os
import time
import json
from pathlib import Path
from typing import Any, Dict
from datetime import datetime


# 日志文件路径配置
LOG_DIR = os.environ.get(
    "SRS_AGENT_LOG_DIR",
    str(Path(__file__).resolve().parent.parent / "logs")
)

LOG_FILE = os.environ.get(
    "SRS_AGENT_LOG_FILE",
    str(Path(LOG_DIR) / "srs-agent.log")
)

# 确保日志目录存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def setup_logger(name: str = "srs_agent", level: int = logging.INFO) -> logging.Logger:
    """
    配置并返回logger实例
    
    Args:
        name: logger名称
        level: 日志级别
        
    Returns:
        配置好的Logger实例
    """
    logger = logging.getLogger(name)
    
    # 如果已有handlers，直接返回
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # 创建格式化器
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    simple_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_state_summary(state: Dict[str, Any], max_length: int = 200) -> str:
    """
    生成状态摘要字符串
    
    Args:
        state: 状态字典
        max_length: 最大长度
        
    Returns:
        状态摘要字符串
    """
    summary = {}
    for key, value in state.items():
        if value is None:
            summary[key] = "None"
        elif isinstance(value, (str, list, dict)):
            if isinstance(value, str):
                summary[key] = f"str({len(value)} chars)"
            elif isinstance(value, list):
                summary[key] = f"list({len(value)} items)"
            elif isinstance(value, dict):
                summary[key] = f"dict({len(value)} keys)"
        else:
            summary[key] = f"{type(value).__name__}"
    
    return json.dumps(summary, ensure_ascii=False, indent=2)


def log_node_execution(func):
    """
    节点执行装饰器 - 自动记录节点的输入、输出、耗时和异常
    
    功能：
    1. 记录节点开始执行
    2. 记录输入状态摘要
    3. 记录执行耗时
    4. 记录输出状态变化
    5. 记录异常信息（如有）
    
    Usage:
        @log_node_execution
        def my_agent_node(state: SRSState) -> SRSState:
            ...
    """
    @functools.wraps(func)
    def wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
        logger = setup_logger(f"srs_agent.{func.__name__}")
        node_name = func.__name__
        
        # 记录开始时间
        start_time = time.time()
        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # 记录节点开始
        logger.info("=" * 80)
        logger.info(f"▶️  开始执行节点: {node_name}")
        logger.info(f"   时间: {start_datetime}")
        logger.info("-" * 80)
        
        # 记录输入状态摘要
        logger.info("📥 输入状态:")
        try:
            state_summary = get_state_summary(state)
            logger.info(f"   {state_summary}")
        except Exception as e:
            logger.warning(f"   无法生成状态摘要: {e}")
        
        # 记录关键输入数据
        _log_key_inputs(logger, state)
        
        logger.info("-" * 80)
        
        try:
            # 执行节点函数
            result = func(state)
            
            # 计算耗时
            end_time = time.time()
            duration = end_time - start_time
            
            # 记录成功
            logger.info("📤 输出状态:")
            try:
                result_summary = get_state_summary(result)
                logger.info(f"   {result_summary}")
            except Exception as e:
                logger.warning(f"   无法生成输出摘要: {e}")
            
            # 记录状态变化
            _log_state_changes(logger, state, result)
            
            logger.info(f"✅ 节点执行成功 | 耗时: {duration:.3f}s")
            logger.info("=" * 80)
            
            return result
            
        except Exception as e:
            # 计算耗时（即使失败）
            end_time = time.time()
            duration = end_time - start_time
            
            # 记录错误
            logger.error(f"❌ 节点执行失败 | 耗时: {duration:.3f}s")
            logger.error(f"   错误类型: {type(e).__name__}")
            logger.error(f"   错误信息: {str(e)}")
            logger.error(f"   堆栈跟踪:", exc_info=True)
            logger.info("=" * 80)
            
            # 重新抛出异常
            raise
    
    return wrapper


def _log_key_inputs(logger: logging.Logger, state: Dict[str, Any]):
    """
    记录关键输入数据
    
    Args:
        logger: logger实例
        state: 状态字典
    """
    # 根据不同节点类型记录不同的关键信息
    node_keys = {
        'input_files': '输入文件列表',
        'template_path': '模板路径',
        'project_dir': '项目目录',
        'current_section_index': '当前章节索引',
        'output_path': '输出路径',
    }
    
    for key, description in node_keys.items():
        if key in state and state[key] is not None:
            value = state[key]
            if isinstance(value, list):
                logger.info(f"   📌 {description}: {len(value)} 项")
                if len(value) <= 5:  # 只展示少量项目
                    for i, item in enumerate(value, 1):
                        logger.info(f"      {i}. {item}")
            else:
                logger.info(f"   📌 {description}: {value}")


def _log_state_changes(logger: logging.Logger, old_state: Dict[str, Any], new_state: Dict[str, Any]):
    """
    记录状态变化
    
    Args:
        logger: logger实例
        old_state: 旧状态
        new_state: 新状态
    """
    # 找出新增或修改的键
    changed_keys = []
    for key in new_state:
        if key not in old_state:
            changed_keys.append((key, "新增"))
        elif old_state[key] != new_state[key]:
            changed_keys.append((key, "修改"))
    
    if changed_keys:
        logger.info("🔄 状态变化:")
        for key, change_type in changed_keys:
            new_value = new_state[key]
            if isinstance(new_value, (str, int, float, bool)):
                logger.info(f"   {change_type} [{key}]: {new_value}")
            elif isinstance(new_value, list):
                logger.info(f"   {change_type} [{key}]: list({len(new_value)} items)")
            elif isinstance(new_value, dict):
                logger.info(f"   {change_type} [{key}]: dict({len(new_value)} keys)")
            else:
                logger.info(f"   {change_type} [{key}]: {type(new_value).__name__}")


def log_workflow_start(workflow_name: str = "SRS Workflow"):
    """
    记录工作流开始
    
    Args:
        workflow_name: 工作流名称
    """
    logger = setup_logger("srs_agent.workflow")
    logger.info("\n" + "🚀" * 40)
    logger.info(f"工作流启动: {workflow_name}")
    logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("🚀" * 40 + "\n")


def log_workflow_end(success: bool = True, total_duration: float = 0):
    """
    记录工作流结束
    
    Args:
        success: 是否成功
        total_duration: 总耗时（秒）
    """
    logger = setup_logger("srs_agent.workflow")
    if success:
        logger.info("\n" + "✨" * 40)
        logger.info(f"工作流执行成功!")
        logger.info(f"总耗时: {total_duration:.3f}s ({total_duration/60:.2f}分钟)")
        logger.info("✨" * 40 + "\n")
    else:
        logger.error("\n" + "💥" * 40)
        logger.error(f"工作流执行失败!")
        logger.error(f"已执行时间: {total_duration:.3f}s")
        logger.error("💥" * 40 + "\n")


# 便捷函数
def log_debug(message: str):
    """记录调试日志"""
    setup_logger("srs_agent").debug(message)


def log_info(message: str):
    """记录信息日志"""
    setup_logger("srs_agent").info(message)


def log_warning(message: str):
    """记录警告日志"""
    setup_logger("srs_agent").warning(message)


def log_error(message: str, exc: Exception = None):
    """记录错误日志"""
    logger = setup_logger("srs_agent")
    if exc:
        logger.error(message, exc_info=True)
    else:
        logger.error(message)


# 导出所有需要的函数和装饰器
__all__ = [
    'setup_logger',
    'log_node_execution',
    'log_workflow_start',
    'log_workflow_end',
    'log_debug',
    'log_info',
    'log_warning',
    'log_error',
    'get_state_summary',
]
