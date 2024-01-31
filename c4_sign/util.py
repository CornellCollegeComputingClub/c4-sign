import time

import requests

def ttl_cache(ttl_seconds):
    def decorator(func):
        cache = {}
        def wrapper(*args, **kwargs):
            cache_key = (func.__name__,) + tuple(args) + tuple(kwargs.items())
            now = time.time()
            cached_result = cache.get(cache_key)
            if cached_result is None or now - cached_result['timestamp'] > ttl_seconds:
                cached_result = func(*args, **kwargs)
                cache[cache_key] = {'result': cached_result, 'timestamp': now}
                return cached_result
            return cached_result['result']
        wrapper.clear_cache = lambda: cache.clear()
        return wrapper
    return decorator

def internet_is_available():
    try:
        requests.get("https://google.com", timeout=1)
        return True
    except requests.exceptions.ConnectionError:
        return False

@ttl_cache(60 * 60) # 1 hour
def requests_get_1hr_cache(url, **kwargs):
    return requests.get(url, **kwargs)
