import logging
import sys
from src.config import LOGS_DIR

def setup_logger(name: str = "SalesBI") -> logging.Logger:
    """
    Configures and returns a thread-safe logger writing to both stdout and logs/app.log.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding duplicate handlers if logger is already configured
    if logger.handlers:
        return logger

    # Log format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    log_file_path = LOGS_DIR / "app.log"
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Global app logger instance
logger = setup_logger()
