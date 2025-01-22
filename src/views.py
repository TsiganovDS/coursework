import json

import pandas as pd

from src.logger import setting_logger
from src.utils import (
    dat,
    fetch_exchange_rates,
    filter_transactions_by_card,
    filter_transactions_by_date,
    get_greeting,
    get_stocks,
    get_top_transactions,
)

logger = setting_logger("views")


def generator_json_data(df_transactions: pd.DataFrame, end_date: str) -> str:
    """Функция формирует json ответ для главной страницы SkyBank"""
    logger.info("Функция начала свою работу.")
    try:
        greeting = get_greeting()
        top_5_tr = get_top_transactions(df_transactions)
        filter_transactions = filter_transactions_by_card(df_transactions, end_date)
        currency_rates = fetch_exchange_rates(dat)
        stock_price = get_stocks(dat)

        json_data = json.dumps(
            {
                "greeting": greeting,
                "cards": filter_transactions,
                "top_transactions": top_5_tr,
                "currency_rates": currency_rates,
                "stock_prices": stock_price,
            },
            indent=4,
            ensure_ascii=False,
        )
        logger.info("Функция успешно завершила свою работу.")
        return json_data

    except Exception as e:
        logger.error(f"Произошла ошибка в функции generator_json_data: {e}")
        return json.dumps({"error": "Произошла ошибка при генерации данных."}, ensure_ascii=False)
