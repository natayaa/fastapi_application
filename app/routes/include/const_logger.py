from loguru import logger
import sys, logging

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def configure_logger():
    # Clear existing root handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set up basic configuration with InterceptHandler for root logger
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)

    # Clear and set up InterceptHandler for all other loggers
    for name in logging.root.manager.loggerDict.keys():
        logger_instance = logging.getLogger(name)
        logger_instance.handlers = [InterceptHandler()]
        logger_instance.propagate = False  # Prevent propagation to avoid double logging

    # Configure Loguru
    logger.remove()
    logger.add(sys.stdout, level="DEBUG")