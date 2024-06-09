def ensure_throw(func, *args, **kwargs):
    result, exception = func(*args, **kwargs)
    if not result:
        raise exception
