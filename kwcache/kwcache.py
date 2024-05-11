import inspect
from typing import Any
from functools import _make_key


class CacheWrapBase:
    def __init__(self, f: callable, max_size, max_key_call, typed) -> None:
        self.f = f
        self.max_size = max_size
        self.max_key_call = max_key_call
        self.typed = typed
        self.STORAGE = dict()

    def clean_cache(self):
        self.STORAGE = dict()

    def _add_key(self, key, result):
        self.STORAGE.update({key: [result, 1]})
    
    def _get_result(self, key):
        return self.STORAGE.get(key)
    
    def _get_result_and_run_need(self, key):
        if self.max_size == 0 and self.max_key_call == 0:
            return None, True
        
        if self.max_size != 0 and len(self.STORAGE) > self.max_size:
            self.clean_cache()
            return None, True
        
        if not key in self.STORAGE:
            return None, True
        
        res = self.STORAGE[key]

        if self.max_key_call != 0 and res[1] >= self.max_key_call:
            return None, True
        
        return res, False
        
    
class CacheWrap(CacheWrapBase):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        key = _make_key(args, kwargs, self.typed)
        res, need_to_run = self._get_result_and_run_need(key)
        if need_to_run:
            res = self.f(*args, **kwargs)
            self._add_key(key, res)
            return res
        res[1] += 1
        return res[0]


class AsyncCacheWrap(CacheWrapBase):
    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        key = _make_key(args, kwargs, self.typed)
        res, need_to_run = self._get_result_and_run_need(key)
        if need_to_run:
            res = await self.f(*args, **kwargs)
            self._add_key(key, res)
            return res
        res[1] += 1
        return res[0]
    

def kwcache(max_size: int = 0, max_key_call: int = 0, typed: bool = False):
    def wrap(f: callable):
        if inspect.iscoroutinefunction(f):
            return AsyncCacheWrap(f, max_size, max_key_call, typed)
        return CacheWrap(f, max_size, max_key_call, typed)
    
    return wrap
