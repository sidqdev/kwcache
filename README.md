## kwcache - make cache easy

```python3
from kwcache import kwcache


@kwcache(max_key_call=10)
def a(*args, **kwargs):
    print('test')
    return args, kwargs

for i in range(50):
    a(1, "1", test=1)
    a(2, "2", test=2)
    a(3, "3", test=3)

```

