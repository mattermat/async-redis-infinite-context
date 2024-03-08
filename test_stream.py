import asyncio
import aioredis  # type: ignore
import pytest

from stream import Stream


@pytest.fixture
async def redis():
    """Return redis client instance
    """
    redis = await aioredis.create_redis('redis://localhost')
    yield redis
    await redis.flushall()
    redis.close()


@pytest.mark.asyncio
async def test_run_gathered(redis):
    async def _main():
        values = []
        async with Stream('test_stream_1') as s:
            async for value in s.read():
                try:
                    values.append(value)
                except asyncio.CancelledError:
                    return value

    async def _checker():
        await asyncio.sleep(.1)
        expected_res = []
        for i in range(5):
            expected_res.append(await redis.xadd('test_stream_1', {'x': i}))
        return expected_res

    check_task = asyncio.create_task(_checker())
    stream_task = asyncio.create_task(_main())

    expected_res = await check_task
    print(expected_res)

    res = stream_task.cancel()

    print(stream_task)
    print(res)
    #print(await res)
    #res, expected_res = await asyncio.gather(_main(), _checker())

    for r in res:
        assert r == expected_res[r] 
