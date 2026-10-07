import threading
import time
cache = {}
cache_lock = threading.Lock()
CACHE_TTL=60
def get_response(cache_key):
    with cache_lock:
        if cache_key not in cache:
            return None
        cached_response, cached_time = cache[cache_key]
        if time.time() - cached_time > CACHE_TTL:
            del cache[cache_key]
            return None
        return cached_response
    
def save_response(cache_key, response):
    with cache_lock:
        cache[cache_key] = (bytes(response), time.time())