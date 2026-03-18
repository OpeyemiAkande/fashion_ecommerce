import sys
import logging
import inspect
from typing import Any, Optional, Callable
from loguru import logger


def configure_logger(
    console_level: str = "INFO", log_format: Optional[str] = None
) -> None:
    """
    Configure loguru logger with console and outputs

    Args:
        console_level: Minimum level for console logs
        file_level: Minimum level for file logs
        rotation: When to rotate log files (sizes or time)
        retention: How long to keep log files
        log_format: Optional custom format string
    """

    logger.remove()

    if log_format is None:
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    logger.add(
        sys.stderr,
        format=log_format,
        level=console_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )


class InterceptHandler(logging.Handler):
    """Intercepts standing library logging and redirects to loguru"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def patch_std_logging():
    """Patch all standard library loggers to use loguru"""
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    for name in logging.root.manager.loggerDict.keys():
        logging_logger = logging.getLogger(name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]


def setup_logging(console_level: str = "INFO", intercept_stdlib: bool = True) -> None:
    """Setup logging for the entire application
    Args:
        console_level: Minimum level for console output
        file_level: Minimum level for file output
        intercept_stdlib: Whether to patch standard library logging
    """

    configure_logger(console_level=console_level)

    if intercept_stdlib:
        patch_std_logging()

    logger.configure(extra={"app_name": "decipher-research-agent"})
    logging.info("Logging configured successfully")


def logger_hook(function_name: str, function_call: Callable, arguments: dict[str, Any]):
    """Hook function that wraps the tool execution"""
    logger.info(f"About to call {function_name} with arguments: {arguments}")
    result = function_call(**arguments)
    logger.info(f"Function call completed with result: {result}")
    return result
