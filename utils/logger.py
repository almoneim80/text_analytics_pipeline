import logging
import os


def get_logger(name: str = "app"):
    """
    Creates and returns a configured logger instance.

    This logger writes log messages to both a file and the console.
    The log file is automatically created in a "logs" directory
    located at the project's root.

    Features:
    - Logs are formatted as: "YYYY-MM-DD HH:MM:SS [LEVEL] message".
    - Supports INFO and higher log levels.
    - Prevents duplicate handlers when imported multiple times.
    - Automatically creates the "logs" directory if it does not exist.

    Args:
        name (str, optional): The name of the logger and the log file.
                              Defaults to "app". Each logger name will have
                              its own log file named "<name>.log".

    Returns:
        logging.Logger: A Python logger instance ready for use.

    Example:
        >>> logger = get_logger("my_module")
        >>> logger.info("This is an info message")
        2025-10-17 14:25:00 [INFO] This is an info message
    """
    # root
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    os.makedirs(LOG_DIR, exist_ok=True)

    LOG_FILE = os.path.join(LOG_DIR, f"{name}.log")

    logger = logging.getLogger(name)
    if not logger.handlers:  # Prevent duplicate processing during multiple imports
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
