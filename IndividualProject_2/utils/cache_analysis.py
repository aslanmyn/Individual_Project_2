import logging
from django.core.cache import cache

logger = logging.getLogger('cache')

def log_cache_hit_or_miss(key, value=None):
    cached_value = cache.get(key)
    if cached_value:
        logger.debug(f"Cache HIT for key: {key}")
    else:
        logger.debug(f"Cache MISS for key: {key}")
        if value is not None:
            logger.debug(f"Setting key {key} in cache.")
            cache.set(key, value, timeout=60 * 15)  