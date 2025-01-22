import json
import re

import pandas as pd

from src.logger import setting_logger

logger = setting_logger("services")


def transfers_to_individuals(transactions: pd.DataFrame) -> str:
    try:
        """Функция возвращает JSON с транзакциями переводов физлицам."""
        logger.info("Функция начала свою работу.")
        transactions_dict = transactions.to_dict("records")
        filtered_transactions = list(filter(lambda x: x["Категория"] == "Переводы", transactions_dict))
        transfers = list(filter(lambda x: re.findall(r"\w+\s\w\.", x["Описание"]), filtered_transactions))
        json_data = json.dumps(transfers, ensure_ascii=False, indent=4)
        logger.info("Функция успешно завершила свою работу.")
        return json_data

    except Exception as e:
        logger.error(f"Произошла ошибка в функции transfers_to_individuals: {e}")
        return json.dumps({"error": "Ошибка при обработке транзакций."}, ensure_ascii=False)


def transfers_to_phone(transactions: pd.DataFrame) -> str:
    try:
        """Возвращает JSON со всеми транзакциями, содержащими в описании номера телефонов."""
        logger.info("Функция начала свою работу.")
        phone_pattern = r"\+\d \d{3} \d{3}[- ]\d{2}[- ]\d{2}"
        transactions_dict = transactions.to_dict("records")
        transfers = list(filter(lambda x: re.search(phone_pattern, x["Описание"]), transactions_dict))
        json_data = json.dumps(transfers, ensure_ascii=False, indent=4)
        logger.info("Функция успешно завершила свою работу.")
        return json_data

    except Exception as e:
        logger.error(f"Произошла ошибка в функции transfers_to_phone: {e}")
        return json.dumps({"error": "Ошибка при обработке транзакций."}, ensure_ascii=False)
