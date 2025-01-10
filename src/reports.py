import json
import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.logger import setting_logger

file_json = os.path.join(os.path.dirname(__file__), "..", "logs", "log_file.json")

logger = setting_logger("reports")


def save_to_file_decorator(file_json: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            logger.info("Декоратор записывает полученный результат в файл.")
            with open(file_json, "w", encoding="utf-8") as file:
                json.dump(result.to_dict("records"), file, ensure_ascii=False, indent=4)
            logger.info("Декоратор успешно завершил свою работу.")
            return result

        return wrapper

    return decorator


@save_to_file_decorator(file_json)
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, возвращающая транзакции за 3 месяца по определенной категории."""
    if date is None:
        end_date = datetime.now().date()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    start_date = end_date - relativedelta(months=3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    sorted_transactions_by_date = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    ]
    pd.options.mode.chained_assignment = None
    sorted_transactions_by_date["Дата операции"] = sorted_transactions_by_date["Дата операции"].dt.strftime(
        "%d.%m.%Y %H:%M:%S"
    )
    sorted_transactions_by_category = sorted_transactions_by_date[sorted_transactions_by_date["Категория"] == category]

    return sorted_transactions_by_category
