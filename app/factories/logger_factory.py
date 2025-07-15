import logging


class LoggerFactory:
    _loggers = {}

    @staticmethod
    def get_logger(name, level: int = logging.INFO) -> logging.Logger:
        if name not in LoggerFactory._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(level)

            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    "%(levelname)s: %(asctime)s - %(name)s - %(message)s", "%H:%M:%S"
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)

            LoggerFactory._loggers[name] = logger

        return LoggerFactory._loggers[name]
