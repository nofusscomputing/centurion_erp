import warnings
import functools



def depreciate(
    *,
    depreciated_in: str,
    removed_in: str | None = None,
    replacement: str | None = None,
):
    def decorator(obj):

        msg = f"{obj.__name__} depreciated since v{depreciated_in}"

        if removed_in:
            msg += f", removal will occur in v{removed_in}"

        if replacement:
            msg += f", use {replacement}"

        if isinstance(obj, type):

            original_init = obj.__init__

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
