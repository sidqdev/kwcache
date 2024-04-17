from typing import Any
from functools import _make_key


class CacheWrap:
    def __init__(self, f: callable, max_size, max_key_call, typed) -> None:
        self.f = f
        self.max_size = max_size
        self.max_key_call = max_key_call
        self.typed = typed
        self.STORAGE = dict()

    def clean_cache(self):
        self.STORAGE = dict()

    def _add_key(self, key, result):
        self.STORAGE.update({key: [result, 0]})
    
    def _get_result(self, key):
        return self.STORAGE.get(key)
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self.max_size == 0 and self.max_key_call == 0:
            return self.f(*args, **kwargs)
         
        key = _make_key(args, kwargs, self.typed)
        if self.max_size != 0 and len(self.STORAGE) > self.max_size:
            self.clean_cache()
            res = self.f(*args, **kwargs)
            self._add_key(key, res)
            return res

        res = self._get_result(key)
        if res is None:
            res = self.f(*args, **kwargs)
            self._add_key(key, res)
            return res
        
        if self.max_key_call != 0 and res[1] > self.max_key_call:
            res = self.f(*args, **kwargs)
            self._add_key(key, res)
            return res

        res[1] += 1

        return res[0]
    

def kwcache(max_size: int = 0, max_key_call: int = 0, typed: bool = False):
    def wrap(f: callable):
        return CacheWrap(f, max_size, max_key_call, typed)
    
    return wrap
