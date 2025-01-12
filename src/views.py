import json

import pandas as pd

from src.logger import setting_logger
from src.utils import (dat, fetch_exchange_rates, filter_transactions_by_card, filter_transactions_by_date,
                       get_greeting, get_stocks, get_top_transactions)

logger = setting_logger("views")


def generator_json_data(df_transactions: pd.DataFrame, date_filter: str) -> str:
    """Функция формирует json ответ для главной страницы SkyBank"""
    logger.info("Функция начала свою работу.")
    greeting = get_greeting()
    filter_transactions_by_date_ = filter_transactions_by_date(df_transactions, date_filter)
    filter_transactions_by_card_ = filter_transactions_by_card(filter_transactions_by_date_)
    top_5_tr = get_top_transactions(filter_transactions_by_date_)
    currency_rates = fetch_exchange_rates(dat)
    stock_price = get_stocks(dat)

    json_data = json.dumps(
        {
            "greeting": greeting,
            "cards": filter_transactions_by_card_,
            "top_transactions": top_5_tr,
            "currency_rates": currency_rates,
            "stock_prices": stock_price,
        },
        indent=4,
        ensure_ascii=False,
    )
    logger.info("Функция успешно завершила свою работу.")
    return json_data
