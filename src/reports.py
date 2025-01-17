import json
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.logger import setting_logger

logger = setting_logger("reports")


def save_to_file_decorator(file_log: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            logger.info("Декоратор записывает полученный результат в файл.")
            with open(file_log, "w", encoding="utf-8") as file:
                json.dump(result.to_dict("records"), file, ensure_ascii=False, indent=4)
            logger.info("Декоратор успешно завершил свою работу.")
            return result

        return wrapper

    return decorator


def spending_by_category(df_transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """Функция, возвращающая транзакции за 3 месяца по определенной категории в формате JSON."""
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    start_date = end_date - relativedelta(months=3)

    # Преобразуем столбец "Дата операции" в формат datetime
    df_transactions["Дата операции"] = pd.to_datetime(
        df_transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )

    # Удаляем записи с некорректными датами
    df_transactions = df_transactions.dropna(subset=["Дата операции"])

    sorted_transactions_by_date = df_transactions[
        (df_transactions["Дата операции"] >= start_date)
        & (df_transactions["Дата операции"] <= end_date)
        & (df_transactions["Категория"] == category)  # Фильтруем по категории
    ].sort_values(
        by="Дата операции"
    )  # Сортировка по дате

    sort_dict = sorted_transactions_by_date[["Дата операции", "Сумма операции с округлением", "Категория"]].to_dict(
        orient="records"
    )

    # Преобразуем формат даты в строку
    for record in sort_dict:
        record["Дата операции"] = record["Дата операции"].strftime("%d.%m.%Y %H:%M:%S")

    return sort_dict
