import asyncio

from stream import Stream


async def _main():
    async with Stream('test_stream_1') as s:
        async for value in s.read():
            print(value)


def main() -> int:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main())
    return 0


if __name__ == '__main__':
    exit(main())
