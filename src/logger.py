import logging
import os


def setting_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    path = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(module)s %(funcName)s %(levelname)s: %(message)s",
        filename=os.path.join(path, f"../logs/{name}.log"),
        filemode="w",
        encoding="utf-8",
    )
    return logger
