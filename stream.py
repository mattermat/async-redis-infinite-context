import aioredis  # type: ignore
from typing import Dict
from typing import AsyncGenerator
import asyncio


class Stream:
    def __init__(self, stream_name: str) -> None:
        self.stream_name = str(stream_name)

    async def __aenter__(self) -> Stream:
        self.r = await aioredis.create_redis(
            'redis://localhost'
        )
        self.running = True
        return self

    async def __aexit__(self, exception_type: str, exception: str, traceback: str) -> None:
        self.r.close()

    async def __aiter__(self) -> Stream:
        return self

    def stop(self) -> None:
        self.running = False

    async def read(self) -> AsyncGenerator[bytes, bytes]:
        while self.running:
            res = await self.r.xread(
                [self.stream_name],
                count=1
            )

            for row in res:
                yield row
