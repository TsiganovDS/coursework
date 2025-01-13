import logging
import os


def setting_logger(name: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)

    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(path, exist_ok=True)
    log_file_path = os.path.join(path, f"{name}.log")

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(module)s %(funcName)s %(levelname)s: %(message)s",
        filename=log_file_path,
        filemode="w",
        encoding="utf-8",
    )

    return logger

