"""
SRS Agent - 软件需求规格说明书生成系统
主入口文件
"""

import time
from graph.workflow import build_srs_workflow
from graph.state import SRSState
from utils.logger import setup_logger, log_workflow_start, log_workflow_end


def main():
    """主函数"""
    logger = setup_logger("srs_agent.main")
    
    # 记录工作流开始
    log_workflow_start("SRS Generation Workflow")
    start_time = time.time()
    
    try:
        # 创建工作流
        logger.info("正在初始化工作流...")
        workflow = build_srs_workflow()
        logger.info("工作流初始化成功")
        
        # 初始化状态
        logger.info("正在初始化状态...")
        initial_state = SRSState()
        logger.info("状态初始化完成")
        
        # 执行工作流
        logger.info("开始执行工作流...")
        result = workflow.invoke(initial_state)
        
        # 计算总耗时
        total_duration = time.time() - start_time
        
        # 记录工作流结束
        log_workflow_end(success=True, total_duration=total_duration)
        
        logger.info(f"工作流执行完成，结果已返回")
        return result
        
    except Exception as e:
        total_duration = time.time() - start_time
        log_workflow_end(success=False, total_duration=total_duration)
        logger.error(f"工作流执行失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
