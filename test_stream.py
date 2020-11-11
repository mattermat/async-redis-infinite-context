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
        async with Stream('test_stream_1') as s:
            async for value in s.read():
                # print(value)
                return(value)

    async def _checker():
        await asyncio.sleep(.1)
        a = await redis.xadd('test_stream_1', {'x': 1})
        # print(a)
        await redis.xadd('test_stream_1', {'x': 2})
        return a

    res = await asyncio.gather(_checker(), _main())
    assert res[1][0] == b'test_stream_1'
    assert res[1][1] == res[0]
    assert res[1][2] == {b'x': b'1'}


def test_myoutput(capsys):
    print('ciao')
    captured = capsys.readouterr()
    assert captured.out == 'ciao\n'
    print('next')
    captured = capsys.readouterr()
    assert captured.out == 'next\n'
