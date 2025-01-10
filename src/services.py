import json
import re

import pandas as pd

from src.logger import setting_logger

logger = setting_logger("services")


def transfers_to_individuals(transactions: pd.DataFrame) -> str:
    """Функция возвращает JSON с транзакциями переводов физлицам."""
    logger.info("Функция начала свою работу.")
    transactions_dict = transactions.to_dict("records")
    filtered_transactions = list(filter(lambda x: x["Категория"] == "Переводы", transactions_dict))
    transfers = list(filter(lambda x: re.findall(r"\w+\s\w\.", x["Описание"]), filtered_transactions))
    json_data = json.dumps(transfers, ensure_ascii=False, indent=4)
    logger.info("Функция успешно завершила свою работу.")
    return json_data


def transfers_to_phone(transactions: pd.DataFrame) -> str:
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""
    logger.info("Функция начала свою работу.")
    transactions_dict = transactions.to_dict("records")
    transfers = list(filter(lambda x: re.findall(r"\D+\+\d\s\d\d\d\s\d+", x["Описание"]), transactions_dict))
    json_data = json.dumps(transfers, ensure_ascii=False, indent=4)
    logger.info("Функция успешно завершила свою работу.")
    return json_data
