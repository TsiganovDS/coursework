import logging
import os

file_l = os.path.join(os.path.dirname(__file__), "..", "logs", "log_file.log")


def setting_logger(message):
    logger = logging.getLogger('name')  # Уникальное имя логгера
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    file_handler = logging.FileHandler(file_l, "w", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info(message)
    return logger
