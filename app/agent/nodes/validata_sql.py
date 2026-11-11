import asyncio
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def validata_sql(state:DataAgentState,runtime:Runtime[DataAgentContext]):

    # 获取流对象
    writer = runtime.stream_writer
    # 输出进度信息
    writer({"stage": "过滤表信息"})
    # 获取sql语句
    sql = state["sql"]
    try:

        # 获取repository
        dw_mysql_repository= runtime.context["dw_mysql_repository"]
        # 验证sql
        await dw_mysql_repository.validate_sql(sql)

        logger.info(f"sql验证正确：{sql}")
        return {"error":None}
    except Exception as e:
        logger.info(f"sql验证失败：{sql}")
        return {"error": f"校验sql异常：str{str(e)}"}

