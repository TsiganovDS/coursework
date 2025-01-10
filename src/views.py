import json

import pandas as pd

from src.logger import setting_logger
from src.utils import (fetch_exchange_rates, fetch_stock_prices, filter_transactions_by_card,
                       filter_transactions_by_date, get_greeting, get_top_transactions)

logger = setting_logger("views")


def generator_json_data(df_transactions: pd.DataFrame, date_filter: str) -> str:
    """Функция формирует json ответ для главной страницы SkyBank"""
    logger.info("Функция начала свою работу.")
    greeting = get_greeting()
    filter_transactions_by_date_ = filter_transactions_by_date(df_transactions, date_filter)
    filter_transactions_by_card_ = filter_transactions_by_card(filter_transactions_by_date_)
    top_5_tr = get_top_transactions(filter_transactions_by_date_)
    exchange_rates = fetch_exchange_rates()
    stock_prices = fetch_stock_prices()

    json_data = json.dumps(
        {
            "greeting": greeting,
            "cards": filter_transactions_by_card_,
            "top_transactions": top_5_tr,
            "currency_rates": exchange_rates,
            "stock_prices": stock_prices,
        },
        indent=4,
        ensure_ascii=False,
    )
    logger.info("Функция успешно завершила свою работу.")
    return json_data
