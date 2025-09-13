import logging
import logging.handlers



class CenturionLogger(logging.Logger):

    EMERG    = 90
    ALERT    = 80
    CRITICAL = 70
    ERROR    = 60
    WARNING  = 50
    WARN     = WARNING
    NOTICE   = 40
    INFO     = 30
    DEBUG    = 20
    TRACE    = 10
    NOTSET = logging.NOTSET

    _levelToName = {
        EMERG:    "EMERG",
        ALERT:    "ALERT",
        CRITICAL: "CRITICAL",
        ERROR:    "ERROR",
        WARNING:  "WARNING",
        NOTICE:   "NOTICE",
        INFO:     "INFO",
        DEBUG:    "DEBUG",
        TRACE:    "TRACE",
        NOTSET:   "NOTSET",
    }

    _nameToLevel = {name: level for level, name in _levelToName.items()}

    def __init__(self, name, level=DEBUG, address="/dev/log"):
        super().__init__(name, level)

        # Attach SysLogHandler
        handler = logging.handlers.SysLogHandler(address=address)
        handler.priority_map.update({
            "EMERG":    "emerg",
            "ALERT":    "alert",
            "CRITICAL": "crit",
            "ERROR":    "err",
            "WARNING":  "warning",
            "NOTICE":   "notice",
            "INFO":     "info",
            "DEBUG":    "debug",
            "TRACE":    "debug",
        })

        # Use a custom Formatter that maps numeric levels to names from this instance only
        formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")
        formatter.format = lambda record: self._levelToName.get(record.levelno, record.levelno) + ": " + record.getMessage()
        handler.setFormatter(formatter)

        self.addHandler(handler)

    # --- Override base class methods ---
    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.CRITICAL):
            self._log(self.CRITICAL, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.ERROR):
            self._log(self.ERROR, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.WARNING):
            self._log(self.WARNING, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.INFO):
            self._log(self.INFO, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.DEBUG):
            self._log(self.DEBUG, msg, args, **kwargs)

    # --- Additional syslog levels ---
    def emergency(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.EMERG):
            self._log(self.EMERG, msg, args, **kwargs)

    def alert(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.ALERT):
            self._log(self.ALERT, msg, args, **kwargs)

    def notice(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.NOTICE):
            self._log(self.NOTICE, msg, args, **kwargs)

    def makeRecord(
        self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None
    ):
        record = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        # Override record.levelname from instance _levelToName
        record.levelname = self._levelToName.get(record.levelno, str(record.levelno))
        return record
