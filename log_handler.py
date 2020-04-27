import logging
from logging import Handler

import coloredlogs


def on_error(logger=None, target_handler=None, capacity=None, level_override=None):
    if logger is None:
        logger = logging.getLogger('')
    if target_handler is None:
        target_handler = logging.StreamHandler()
    if capacity is None:
        capacity = 100
    if level_override is None:
        level_override = logging.DEBUG

    target_handler.setLevel(level_override)
    fmt = '%(asctime)s %(filename)s:%(lineno)s %(funcName)s [%(levelname)s] %(message)s'

    target_handler.setFormatter(coloredlogs.ColoredFormatter(fmt))
    logger.setLevel(level_override)
    handler = RecentHandler(capacity, target=target_handler)

    def decorator(fn):
        def wrapper(*args, **kwargs):
            logger.addHandler(handler)
            caught_exception = False
            try:
                return fn(*args, **kwargs)
            except Exception:
                caught_exception = True
                raise
            finally:
                if caught_exception:
                    logger.info('', extra={'skip_in_recent': True})
                    logger.info('### Log Handler caught exception. Flushing logs:', extra={'skip_in_recent': True})
                    logger.info('', extra={'skip_in_recent': True})
                    handler.flush()
                else:
                    handler.close()
                logger.removeHandler(handler)

        return wrapper

    return decorator


class RecentHandler(Handler):
    """
    Keeps track of most recent `capacity` number of logs. Only emits them when flush() is called.
    """

    def __init__(self, capacity: int, target: Handler):
        """
        Initialize the handler with the buffer size and a target.
        """
        Handler.__init__(self)
        self.capacity = capacity
        self.target = target
        self.buffer = []

    def emit(self, record):
        """Append the record instead of emitting it."""
        if getattr(record, "skip_in_recent", False):
            return
        self.buffer.append(record)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def setTarget(self, target: Handler):
        self.target = target

    def flush(self):
        """
        Flushing means just sending the buffered records to the target, if there is one. This should be called
        externally due to some event.

        The record buffer is also cleared by this operation.
        """
        self.acquire()
        try:
            if self.target:
                for record in self.buffer:
                    self.target.handle(record)
                self.buffer = []
        finally:
            self.release()

    def close(self):
        self.target = None
        self.buffer = []
        self.acquire()
        try:
            Handler.close(self)
        finally:
            self.release()
