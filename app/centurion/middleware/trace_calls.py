import sys
import os
import time
import uuid
import logging
import inspect

from contextlib import contextmanager

from django.conf import settings
from django.db import connection
from django.utils.deprecation import MiddlewareMixin

from rest_framework import serializers

from centurion.logging import CenturionLogger


class TraceCallsMiddleware(MiddlewareMixin):
    """
    Middleware that traces Django request/response cycle:
    - Request metadata (method, path, user, remote addr)
    - Function calls + returns with args, locals, duration
    - DB queries with duration
    - View execution duration
    - Serializer duration
    - Response size
    """

    _app_path: str

    _logger: CenturionLogger

    def __init__(self, get_response=None):

        super().__init__(get_response)

        self._app_path = os.path.join(settings.BASE_DIR, "")

        self._logger = logging.getLogger('centurion').getChild('trace')

        self.start_times = {}

        self.request_id = None



    def _safe_locals(self, frame):
        snapshot = {}
        keys = list(frame.f_locals.keys())
        for k in keys:
            try:
                snapshot[k] = repr(frame.f_locals[k])[:100]
            except Exception:
                snapshot[k] = "<unrepresentable>"
        return snapshot




    def _log_trace(self,
        trace_type: str,
        function_name: str = '',
        class_name: str = '',
        caller: str = '',
        duration = 0,
        file_path: str = '',
        line_number: int = 0,
        locals: str = '',
        msg: str = '',
        log_level: int = CenturionLogger.INFO,
        log_slow:bool = False,
    ) -> None:

        if caller:
            caller = f'[from {caller}]'


        if getattr(self, 'request_id', None):

            request_id = self.request_id

        else:

            request_id = ''


        if isinstance(duration, int) or isinstance(duration, float):

            duration_str = f'duration={duration:.6f}s '
            duration = float(duration)

            if log_slow and duration > 0.2 and duration < 0.5 and log_level == CenturionLogger.INFO:

                log_level = CenturionLogger.NOTICE

            elif log_slow and duration >= 0.5 and duration < 1 and log_level == CenturionLogger.INFO:

                log_level = CenturionLogger.WARNING

            elif log_slow and duration >= 1 and log_level == CenturionLogger.INFO:

                log_level = CenturionLogger.ERROR


        else:
            duration_str = f'duration={duration} '


        self._logger.log(
            level = log_level,
            msg = str(
                f'Build[{settings.BUILD_VERSION}]'
                f'[req:{request_id}] '
                f'{trace_type} '
                f'{duration_str} '
                f'{class_name} '
                f'{function_name} '
                f'({file_path}:{line_number}) '
                f'{caller} '
                f'{locals} '
                f': {msg}'
            )
        )


        return


    @contextmanager
    def _db_logger(self):

        def wrapper_execute(execute, sql, params, many, context):

            start = time.perf_counter()

            try:

                return execute(sql, params, many, context)

            finally:

                duration = time.perf_counter() - start

                for frame_info in inspect.stack():

                    if not frame_info.filename.endswith("trace_calls.py"):
                        caller_file = frame_info.filename
                        caller_line = frame_info.lineno
                        break

                else:

                    caller_file = "N/A"

                    caller_line = 0

                self._log_trace(
                    trace_type = 'DB QUERY',
                    duration = duration,
                    file_path = caller_file,
                    line_number = caller_line,
                    msg = f'{sql} {params}',
                    log_level = CenturionLogger.TRACE
                )

        with connection.execute_wrapper(wrapper_execute):
            yield



    def _patch_serializers(self):

        def timed(method):

            def wrapper(serializer, *args, **kwargs):

                start = time.perf_counter()
                result = method(serializer, *args, **kwargs)
                duration = time.perf_counter() - start
                attrs = list(serializer.__dict__.keys())
                locals_snapshot = {}

                for k in attrs:

                    try:

                        locals_snapshot[k] = repr(serializer.__dict__[k])[:100]

                    except Exception:

                        locals_snapshot[k] = "<unrepresentable>"

                self._log_trace(
                    trace_type = 'SERIALIZER',
                    function_name = method.__name__,
                    class_name = serializer.__class__.__name__,
                    duration = duration,
                    file_path = f"{serializer.__class__.__module__.replace('.', '/')}.py",
                    line_number = 0,
                    locals = locals_snapshot,
                )


                return result

            return wrapper

        serializers.Serializer.to_representation = timed(
            serializers.Serializer.to_representation
        )
        serializers.Serializer.run_validation = timed(
            serializers.Serializer.run_validation
        )



    def _trace_calls(self, frame, event, arg):

        filename = frame.f_code.co_filename

        if not filename.startswith(self._app_path):
            return self._trace_calls

        if filename.endswith("trace_calls.py"):
            return self._trace_calls

        func_name = frame.f_code.co_name
        lineno = frame.f_lineno
        key = (id(frame), func_name)
        locals_snapshot = ''
        caller_info = ''
        msg = ''
        duration = 0
        log_level = CenturionLogger.INFO
        log_slow = True

        if frame.f_back:

            caller_code = frame.f_back.f_code
            caller_name = caller_code.co_name
            caller_file = caller_code.co_filename
            caller_line = frame.f_back.f_lineno
            caller_info = f"{caller_name} ({caller_file}:{caller_line})"

        else:
            caller_info = "N/A"


        if event == "call":

            self.start_times[key] = time.perf_counter()
            locals_snapshot = self._safe_locals(frame)
            duration = 'START'

        else:

            if event == "return":

                msg = repr(arg)[:200]

                start_time = self.start_times.pop(key, None)
                log_slow = True

                if start_time is not None:
                    duration = time.perf_counter() - start_time


            elif event == "line":

                log_level = CenturionLogger.DEBUG


        self._log_trace(
            trace_type = str(event).upper(),
            function_name = func_name,
            caller = caller_info,
            duration = duration,
            file_path = filename,
            line_number = lineno,
            locals = locals_snapshot,
            msg = msg,
            log_level = log_level,
            log_slow = log_slow,
        )

        return self._trace_calls



    def __call__(self, request):

        if not getattr(settings, 'TRACE_LOGGING', False):
            return self.get_response(request)


        self.request_id = uuid.uuid4().hex
        sys.settrace(self._trace_calls)

        user = getattr(request, "user", None)
        username = user.username if user and user.is_authenticated else "anon"
        client_ip = request.META.get("REMOTE_ADDR")

        self._log_trace(
            trace_type = f'REQUEST {request.method} {request.get_full_path()}',
            # request_id = self.request_id,
            # function_name = None,
            # class_name = None,
            # caller = None,
            # duration = None,
            # file_path = None,
            # line_number = None,
            # locals = None,
            msg = f'from {client_ip} user={username}'
        )


        start_view = time.perf_counter()
        self._patch_serializers()

        try:

            with self._db_logger():

                response = self.get_response(request)

        finally:
            sys.settrace(None)
            self.start_times.clear()


        view_duration = time.perf_counter() - start_view
        response_size = len(getattr(response, "content", b"") or b"")

        if hasattr(request, "resolver_match") and request.resolver_match:

            view_func = request.resolver_match.func
            view_class_name = getattr(view_func, "view_class", view_func.__class__).__name__
            view_file = getattr(sys.modules[view_func.__module__], "__file__", "N/A")

        else:

            view_class_name = "N/A"
            view_file = "N/A"

        log_level = CenturionLogger.INFO
        if float(view_duration) > 1:
            log_level = CenturionLogger.WARN

        self._log_trace(
            trace_type = 'VIEW',
            class_name = view_class_name,
            duration = view_duration,
            file_path = view_file,
            msg = f'response_size={response_size} byte',
            log_level = log_level,
            log_slow = True,
        )

        return response
