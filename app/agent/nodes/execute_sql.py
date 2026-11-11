import asyncio
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def execute_sql(state:DataAgentState,runtime:Runtime[DataAgentContext]):
    # 获取流对象
    writer = runtime.stream_writer
    # 输出进度信息
    writer({"stage": "执行sql"})
    try:
    # 获取sql语句
        sql = state["sql"]
        # repository
        dw_mysql_repository= runtime.context["dw_mysql_repository"]

        # 执行 [{"销售总额"：41099.5}]
        result=await dw_mysql_repository.execute_sql(sql)
        # 输出结果
        writer({"result":result})
        logger.info(f"执行sql成功：{result}")

        return {"result": result}

    except Exception as e:
        logger.error(f"执行sql异常：{str(e)}")
        raise