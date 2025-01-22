import json
import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.logger import setting_logger

logger = setting_logger("reports")

file_rep = os.path.join(os.path.dirname(__file__), "..", "logs", "reports.json")


def save_to_file_decorator(file_rep: Optional[str] = "report.json") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            logger.info("Декоратор записывает полученный результат в файл.")
            # Проверяем, является ли результат списком или DataFrame
            if isinstance(result, list):
                with open(file_rep, "w", encoding="utf-8") as file:
                    json.dump(result, file, ensure_ascii=False, indent=4)
            elif isinstance(result, pd.DataFrame):
                with open(file_rep, "w", encoding="utf-8") as file:
                    json.dump(result.to_dict("records"), file, ensure_ascii=False, indent=4)
            else:
                logger.error("Неверный тип результата: не список и не DataFrame.")
            logger.info("Декоратор успешно завершил свою работу.")
            return result

        return wrapper

    return decorator


@save_to_file_decorator(file_rep)
def spending_by_category(df_transactions: pd.DataFrame, category: str, date: Optional[str] = None):
    """Функция, возвращающая транзакции за 3 месяца по определенной категории в формате JSON."""
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    start_date = end_date - relativedelta(months=3)

    df_transactions["Дата операции"] = pd.to_datetime(
        df_transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )

    df_transactions = df_transactions.dropna(subset=["Дата операции"])

    sorted_transactions_by_date = df_transactions[
        (df_transactions["Дата операции"] >= start_date)
        & (df_transactions["Дата операции"] <= end_date)
        & (df_transactions["Категория"] == category)
    ].sort_values(by="Дата операции")

    if sorted_transactions_by_date.empty:
        logger.warning("Нет транзакций для данной категории за указанный период.")
        return []

    result = sorted_transactions_by_date[["Дата операции", "Сумма операции с округлением", "Категория"]]

    result_list = result.to_dict(orient="records")

    for record in result_list:
        record["Дата операции"] = record["Дата операции"].strftime("%d.%m.%Y %H:%M:%S")

    return result_list
