import asyncio
import aioredis  # type: ignore

from stream import Stream


async def _checker():
    await asyncio.sleep(.1)
    redis = await aioredis.create_redis('redis://localhost')
    a = await redis.xadd('test_stream_1', {'x': 1})
    print(a)
    a = await redis.xadd('test_stream_1', {'x': 2})
    print(a)
    redis.close()


async def _main():
    async with Stream('test_stream_1') as s:
        async for value in s.read():
            s.stop()
            print(value)
            print('ok')


def main() -> int:
    loop = asyncio.get_event_loop()
    run = asyncio.gather(_main(), _checker())
    loop.run_until_complete(run)
    return 0


if __name__ == '__main__':
    exit(main())
