import logging
import os


def setting_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    path = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к текущему файлу
    log_file_path = os.path.join(path, "../logs", f"{name}.log")  # Формируем путь к лог-файлу

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  # Создаём папку, если её нет

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(module)s %(funcName)s %(levelname)s: %(message)s",
        filename=log_file_path,
        filemode="w",
        encoding="utf-8",
    )
    return logger
