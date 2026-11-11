from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DwMysqlRepository:
    def __init__(self,session:AsyncSession):
        self.session=session


    async def get_column_values(self, table_name:str, column_name:str,limit:int =10):
        """
        查询指定字段的取值

        :param table_name:
        :param column_name:
        :return: ["C001","C002","C003","C004","C005"]
        """
        # 定义sql
        sql = f"select distinct {column_name} from {table_name} limit {limit}"
        # 执行sql
        result =await self.session.execute(text(sql))
        # [row(C001),row(C002),row(C003)]
        return result.scalars().fetchall()

    async def get_column_types(self, table_name:str):
        """
        查询表中字段的类型
        :param table_name:
        :return: 字段 {"字段名":"字段类型"}


        """
        # 定义sql
        sql = f"show columns from {table_name}"
        # 执行sql
        result=await self.session.execute(text(sql))
        #[row(),row(),row()]

        # 获取结果，组装数据
        return {row.Field: row.Type for row in result.fetchall()}

    async def get_db_info(self):
        """
        查询数据库信息
        1.版本信息

        2.数据库方言

        :return:
        """
        # 查询数据的版本
        result=await self.session.execute(text("select version()"))
        # 获取版本
        version = result.scalar()

        # 查询数据库方言
        dialect = self.session.bind.dialect.name

        return {"version":version,"dialect":dialect}

    async def validate_sql(self, sql:str):
        """

        使用explain 关键字校验sql
        :param sql:
        :return:
        """

        await  self.session.execute(text(f"explain {sql}"))

    async def execute_sql(self, sql:str):
        """
        执行sql语句
        :param sql:
        :return:
        """
        # [(),(),()]
        result =await self.session.execute(text(sql))
        # 调整格式 [{RowMapping对象（key:value）},{}]
        return [dict(row) for row in result.mappings().fetchall()]


