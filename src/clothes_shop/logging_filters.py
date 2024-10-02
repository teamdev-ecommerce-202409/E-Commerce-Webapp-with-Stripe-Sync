import logging


class DebugOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG


class InfoOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


class WarningOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING


class ErrorOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


class CriticalOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.CRITICAL
