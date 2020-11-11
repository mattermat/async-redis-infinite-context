import aioredis  # type: ignore


class Stream:
    def __init__(self, stream_name: str) -> None:
        self.stream_name = str(stream_name)

    async def __aenter__(self):
        self.r = await aioredis.create_redis(
            'redis://localhost'
        )
        self.running = True
        return self

    async def __aexit__(self, exception_type, exception, traceback):
        self.r.close()

    async def __aiter__(self):
        return self

    def stop(self) -> None:
        self.running = False

    async def read(self):
        while self.running:
            res = await self.r.xread(
                [self.stream_name],
                count=1
            )

            for row in res:
                yield row
