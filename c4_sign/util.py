import time

import requests


def ttl_cache(ttl_seconds):
    def decorator(func):
        cache = {}

        def wrapper(*args, **kwargs):
            cache_key = (func.__name__,) + tuple(args) + tuple(kwargs.items())
            now = time.time()
            cached_result = cache.get(cache_key)
            if cached_result is None or now - cached_result["timestamp"] > ttl_seconds:
                cached_result = func(*args, **kwargs)
                cache[cache_key] = {"result": cached_result, "timestamp": now}
                return cached_result
            return cached_result["result"]

        wrapper.clear_cache = lambda: cache.clear()
        return wrapper

    return decorator


def lerp(a, b, t):
    """
    Linear interpolation between a and b by t.

    :param a: start value
    :param b: end value
    :param t: interpolation factor
    :return: a value between a and b
    """
    return a + (b - a) * t


def map_value(value, in_min, in_max, out_min, out_max):
    """
    Map a value from one range to another.

    :param value: the value to map
    :param in_min: the minimum value of the input range
    :param in_max: the maximum value of the input range
    :param out_min: the minimum value of the output range
    :param out_max: the maximum value of the output range
    :return: the value mapped to the output range
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def internet_is_available():
    try:
        requests.get("https://google.com", timeout=1)
        return True
    except requests.exceptions.ConnectionError:
        return False


@ttl_cache(60 * 60)  # 1 hour
def requests_get_1hr_cache(url, **kwargs):
    return requests.get(url, **kwargs)
