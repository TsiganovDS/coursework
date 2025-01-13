import json
import pandas as pd
from datetime import datetime
from typing import Callable, Any, Optional
from functools import wraps
from dateutil.relativedelta import relativedelta

from src.services import logger
from src.utils import file_json


def save_to_file_decorator(file_json: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(args: Any, *kwargs: Any) -> Any:
            result = func(args, *kwargs)
            logger.info("Декоратор записывает полученный результат в файл.")
            with open(file_json, "w", encoding="utf-8") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
                logger.info("Декоратор успешно завершил свою работу.")
            return result

        return wrapper

    return decorator


@save_to_file_decorator(file_json)  # Укажи путь к файлу
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """Функция, возвращающая транзакции за 3 месяца по определенной категории в формате JSON."""
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    start_date = end_date - relativedelta(months=3)

    # Преобразуем столбец "Дата операции" в формат datetime
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors='coerce')

    # Удаляем записи с некорректными датами
    transactions = transactions.dropna(subset=["Дата операции"])

    sorted_transactions_by_date = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date) &
        (transactions["Категория"] == category)  # Фильтруем по категории
    ]

    sort_dict = sorted_transactions_by_date[["Дата операции", "Сумма операции с округлением", "Категория"]].to_dict(orient='records')

    # Преобразуем формат даты в строку
    for record in sort_dict:
        record['Дата операции'] = record['Дата операции'].strftime("%d.%m.%Y %H:%M:%S")

    return sort_dict
