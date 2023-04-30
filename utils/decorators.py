def with_sleep(time):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            self.after(time)
            fn()
        return wrapper
    return decorator

