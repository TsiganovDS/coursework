import logging
import os

def setting_logger(name: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    path = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к текущему файлу
    logfilepath = os.path.join(path, "../logs", f"{name}.log")  # Формируем путь к лог-файлу

    os.makedirs(os.path.dirname(logfilepath), exist_ok=True)  # Создаём папку, если её нет

    logger.setLevel(level)  # Устанавливаем уровень логирования

    # Формат для логов
    formatter = logging.Formatter("%(asctime)s %(module)s %(funcName)s %(levelname)s: %(message)s")

    # Обработчик для записи в файл
    filehandler = logging.FileHandler(logfile_path, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


    return logger
