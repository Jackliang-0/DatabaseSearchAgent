import yaml
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


async def generate_answer(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    # 获取流对象
    writer = runtime.stream_writer
    # 输出进度信息
    writer({"stage": "生成回答"})
    try:
        # 获取用户的问题
        query = state["query"]
        # 获取执行的sql
        sql = state["sql"]
        # 获取查询结果
        result = state["result"]

        # 构建提示词信息
        prompt = PromptTemplate(template=load_prompt("generate_answer"),
                                input_variables=["query", "sql", "result"])
        # 构建转换器
        output_parser = StrOutputParser()
        # 构建执行链
        chain = prompt | llm | output_parser
        # 执行链，获取自然语言回答
        answer = await chain.ainvoke(
            {
                "query": query,
                "sql": sql,
                "result": yaml.dump(result, allow_unicode=True, sort_keys=False)
            }
        )

        logger.info(f"生成回答成功：{answer}")
        # 输出结果给前端
        writer({"answer": answer})

        return {"answer": answer}
    except Exception as e:
        logger.error(f"生成回答异常：{str(e)}")
        raise
