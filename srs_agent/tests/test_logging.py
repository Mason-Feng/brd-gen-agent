"""
日志系统测试脚本
用于演示和测试日志功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import (
    setup_logger, 
    log_node_execution, 
    log_workflow_start, 
    log_workflow_end,
    log_info,
    log_error
)


# 测试装饰器
@log_node_execution
def test_node_1(state: dict) -> dict:
    """测试节点1"""
    state['result_1'] = 'completed'
    state['data'] = [1, 2, 3, 4, 5]
    return state


@log_node_execution
def test_node_2(state: dict) -> dict:
    """测试节点2"""
    state['result_2'] = 'completed'
    state['metadata'] = {'key1': 'value1', 'key2': 'value2'}
    return state


@log_node_execution
def test_node_error(state: dict) -> dict:
    """测试错误情况"""
    raise ValueError("这是一个测试错误")


def test_basic_logging():
    """测试基本日志功能"""
    print("\n" + "="*80)
    print("测试1: 基本日志记录")
    print("="*80)
    
    logger = setup_logger("test.basic")
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
    
    log_info("使用便捷函数记录日志")


def test_node_decorator():
    """测试节点装饰器"""
    print("\n" + "="*80)
    print("测试2: 节点装饰器")
    print("="*80)
    
    # 测试正常执行
    state = {'input': 'test_data'}
    result = test_node_1(state)
    print(f"节点1执行结果: {result}")
    
    result = test_node_2(result)
    print(f"节点2执行结果: {result}")


def test_error_handling():
    """测试错误处理"""
    print("\n" + "="*80)
    print("测试3: 错误处理")
    print("="*80)
    
    try:
        state = {'input': 'test'}
        test_node_error(state)
    except Exception as e:
        print(f"捕获到异常: {e}")


def test_workflow_logging():
    """测试工作流日志"""
    print("\n" + "="*80)
    print("测试4: 工作流日志")
    print("="*80)
    
    log_workflow_start("Test Workflow")
    
    # 模拟一些工作
    import time
    time.sleep(0.5)
    
    log_workflow_end(success=True, total_duration=0.5)


if __name__ == "__main__":
    print("\n🧪 SRS Agent 日志系统测试")
    print("="*80)
    
    try:
        test_basic_logging()
        test_node_decorator()
        test_error_handling()
        test_workflow_logging()
        
        print("\n" + "="*80)
        print("✅ 所有测试完成！")
        print("="*80)
        print(f"\n📄 请查看日志文件: logs/srs-agent.log")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
