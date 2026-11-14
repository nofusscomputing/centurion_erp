import warnings
import functools



def depreciate(
    *,
    depreciated_in: str,
    removed_in: str | None = None,
    replacement: str | None = None,
    skip_tests: bool = False,
):
    def decorator(obj):

        msg = f"{obj.__name__} depreciated since v{depreciated_in}"

        if removed_in:
            msg += f", removal will occur in v{removed_in}"

        if replacement:
            msg += f", use {replacement}"

        if isinstance(obj, type):

            original_init = obj.__init__


            if not hasattr(obj, '_decorator'):
                obj._decorator = []

            obj._decorator.append({
                'name': 'depreciate',
                'kwargs': {
                    'depreciated_in': depreciated_in,
                    'removed_in': removed_in,
                    'replacement': replacement,
                    'skip_tests': skip_tests,
                }
            })

            if skip_tests:

                obj.decorator_depreciated = True


            @functools.wraps(original_init)
            def wrapped_init(self, *args, **kwargs):

                warnings.warn(
                    msg,
                    DeprecationWarning,
                    stacklevel=2,
                )

                return original_init(self, *args, **kwargs)

            obj.__init__ = wrapped_init
            return obj

        @functools.wraps(obj)
        def wrapper(*args, **kwargs):

            warnings.warn(
                msg,
                DeprecationWarning,
                stacklevel=2,
            )

            return obj(*args, **kwargs)

        return wrapper

    return decorator
