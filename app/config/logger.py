from app.factories import LoggerFactory


class Logger:
    @staticmethod
    def info(name: str, message: str):
        LoggerFactory.get_logger(name).info(message)

    @staticmethod
    def warning(name: str, message: str):
        LoggerFactory.get_logger(name).warning(message)

    @staticmethod
    def error(name: str, message: str):
        LoggerFactory.get_logger(name).error(message)

    @staticmethod
    def debug(name: str, message: str):
        LoggerFactory.get_logger(name).debug(message)
