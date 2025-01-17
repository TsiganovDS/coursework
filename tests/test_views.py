import json
import unittest.mock
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import generator_json_data

expected = {
    "greeting": "Доброе утро!",
    "cards": {"cards_info": 1234},
    "top_transactions": {"transactions": 1234},
    "currency_rates": {"USD": 90},
    "stock_prices": {"APPL": 1500},
}
expected_json = json.dumps(expected, indent=4, ensure_ascii=False)
transactions = pd.DataFrame(
    [
        {
            "Дата операции": "28.03.2018 09:24:15",
            "Дата платежа": "29.03.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -150.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -150.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Связь",
            "MCC": 4814.0,
            "Описание": "МТС",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 150.0,
        },
        {
            "Дата операции": "28.03.2018 08:23:56",
            "Дата платежа": "30.03.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -197.7,
            "Валюта операции": "RUB",
            "Сумма платежа": -197.7,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Billa",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 197.7,
        },
    ]
)


@patch("src.views.get_stocks")
@patch("src.views.fetch_exchange_rates")
@patch("src.views.filter_transactions_by_date")
@patch("src.views.get_top_transactions")
@patch("src.views.filter_transactions_by_card")
@patch("src.views.get_greeting")
def test_views(
    mock_views_get_greeting: unittest.mock.Mock,
    mock_views_filter_transactions_by_card: unittest.mock.Mock,
    mock_views_top_five_transactions: unittest.mock.Mock,
    mock_stocks: unittest.mock.Mock,
    mock_views_exchange_rates: unittest.mock.Mock,
    mock_views_get_stocks: unittest.mock.Mock,
) -> None:
    mock_views_get_greeting.return_value = "Доброе утро!"
    mock_views_filter_transactions_by_card.return_value = {"cards_info": 1234}
    mock_views_top_five_transactions.return_value = {"transactions": 1234}
    mock_stocks.return_value = ["USD", "EUR"]
    mock_views_exchange_rates.return_value = {"USD": 90}
    mock_views_get_stocks.return_value = {"APPL": 1500}
    assert generator_json_data(transactions, "06.07.2024 10:42:30") == expected_json


def test_views_with_wrong_date() -> None:
    with pytest.raises(Exception) as exc_info:
        generator_json_data(transactions, "ABC")
        assert str(exc_info.value) == []
