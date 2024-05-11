import asyncio
from kwcache import kwcache


@kwcache(max_key_call=5)
def test(*args, **kwargs):
    print('test')
    return args, kwargs

for i in range(15):
    test(1, "1", test=1)
    test(2, "2", test=2)
    test(3, "3", test=3)


@kwcache(max_key_call=5)
async def atest(*args, **kwargs):
    print('test')
    return args, kwargs

for i in range(15):
    asyncio.run(atest(1, "1", test=1))
    asyncio.run(atest(2, "2", test=2))
    asyncio.run(atest(3, "3", test=3))


