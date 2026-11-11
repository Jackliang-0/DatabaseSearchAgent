import asyncio
from typing import Optional

from dns.entropy import pool
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker

from app.conf.app_config import app_config, DBConfig


class MysqlClientManager:
    def __init__(self, config: DBConfig):
        self.engine: Optional[AsyncEngine] = None
        self.config = config
        self.session_factory=None

    def _get_url(self):
        return f"mysql+asyncmy://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.database}?charset=utf8mb4"

    def init(self):
        self.engine = create_async_engine(
            url=self._get_url(),
            pool_size =5,
            pool_pre_ping= True
        )
        self.session_factory=async_sessionmaker(
            bind=self.engine,
            autoflush=True,
            autobegin=True,
            expire_on_commit=False
        )

    async def close(self):
        await self.engine.dispose()


dw_mysql_client_manager = MysqlClientManager(app_config.db_dw)
meta_mysql_client_manager = MysqlClientManager(app_config.db_meta)

if __name__ == '__main__':
    # 初始化客户端
    dw_mysql_client_manager.init()


    # 定义异步函数
    async def test():
        # 获取session
        # async with AsyncSession(bind=dw_mysql_client_manager.engine, autoflush=True, autobegin=True, expire_on_commit=True) as session:
        async with dw_mysql_client_manager.session_factory() as session:
            # 执行操作
            sql = "select *from fact_order limit 10"
            # 执行sql
            result = await session.execute(text(sql))

            # 获取结果
            # rows = result.mappings().fetchall()
            rows = result.scalars().fetchall()
            # rows = result.fetchall()
            print(type(rows))
            print(rows)
        await dw_mysql_client_manager.close()
    # 执行异步函数
    asyncio.run(test())
