from unittest.mock import MagicMock, Mock, mock_open, patch

import pandas as pd
import pytest
import requests
from freezegun import freeze_time

from src.utils import (fetch_exchange_rates, filter_transactions_by_card, filter_transactions_by_date, get_greeting,
                       get_stocks, get_top_transactions, load_data_from_excel, load_json)


@pytest.mark.parametrize(
    "mock_data, expected_result",
    [
        (
            {
                "Дата операции": ["31.12.2021 16:44:00"],
                "Дата платежа": ["31.12.2021"],
                "Номер карты": ["*7197"],
                "Статус": "Ok",
                "Сумма операции": ["-160.89"],
                "Валюта операции": ["RUB"],
                "Сумма платежа": ["-160.89"],
                "Валюта платежа": ["RUB"],
            },
            pd.DataFrame(
                {
                    "Дата операции": ["31.12.2021 16:44:00"],
                    "Дата платежа": ["31.12.2021"],
                    "Номер карты": ["*7197"],
                    "Статус": "Ok",
                    "Сумма операции": ["-160.89"],
                    "Валюта операции": ["RUB"],
                    "Сумма платежа": ["-160.89"],
                    "Валюта платежа": ["RUB"],
                }
            ),
        ),
        (
            {
                "Дата операции": ["01.01.2022 12:00:00"],
                "Дата платежа": ["01.01.2022"],
                "Номер карты": ["*1234"],
                "Статус": "Failed",
                "Сумма операции": ["-50.00"],
                "Валюта операции": ["USD"],
                "Сумма платежа": ["-50.00"],
                "Валюта платежа": ["USD"],
            },
            pd.DataFrame(
                {
                    "Дата операции": ["01.01.2022 12:00:00"],
                    "Дата платежа": ["01.01.2022"],
                    "Номер карты": ["*1234"],
                    "Статус": "Failed",
                    "Сумма операции": ["-50.00"],
                    "Валюта операции": ["USD"],
                    "Сумма платежа": ["-50.00"],
                    "Валюта платежа": ["USD"],
                }
            ),
        ),
    ],
)
def test_load_data_from_excel(mock_data, expected_result) -> None:
    df = pd.DataFrame(mock_data)

    with patch("pandas.read_excel", return_value=df) as mock_read_excel:
        result = load_data_from_excel("mock_file.xlsx")
        pd.testing.assert_frame_equal(result, expected_result)
        mock_read_excel.assert_called_once_with("mock_file.xlsx")


@pytest.mark.parametrize(
    "frozen_time, expected_greeting",
    [
        ("2024-01-01 07:00:00", "Доброе утро"),
        ("2024-01-01 13:00:00", "Добрый день"),
        ("2024-01-01 19:00:00", "Добрый вечер"),
        ("2024-01-01 00:00:00", "Доброй ночи"),
    ],
)
def test_get_greeting(frozen_time, expected_greeting) -> None:
    with freeze_time(frozen_time):
        assert get_greeting() == expected_greeting

    @pytest.mark.parametrize(
        "mock_data, expected_result",
        [
            (
                {
                    "Дата платежа": [
                        pd.Timestamp("2023-01-01"),
                        pd.Timestamp("2023-01-02"),
                        pd.Timestamp("2023-01-03"),
                        pd.Timestamp("2023-01-04"),
                        pd.Timestamp("2023-01-05"),
                        pd.Timestamp("2023-01-06"),
                    ],
                    "Сумма операции": [100.50, 200.75, 50.00, 300.00, 150.25, 400.00],
                    "Категория": ["Food", "Transport", "Entertainment", "Food", "Transport", "Entertainment"],
                    "Описание": ["Lunch", "Bus ticket", "Movie", "Dinner", "Taxi", "Concert"],
                },
                [
                    {"date": "06.01.2023", "amount": 400.00, "category": "Entertainment", "description": "Concert"},
                    {"date": "04.01.2023", "amount": 300.00, "category": "Food", "description": "Dinner"},
                    {"date": "02.01.2023", "amount": 200.75, "category": "Transport", "description": "Bus ticket"},
                    {"date": "05.01.2023", "amount": 150.25, "category": "Transport", "description": "Taxi"},
                    {"date": "01.01.2023", "amount": 100.50, "category": "Food", "description": "Lunch"},
                ],
            ),
            (
                {
                    "Дата платежа": [],
                    "Сумма операции": [],
                    "Категория": [],
                    "Описание": [],
                },
            ),
        ],
    )
    @patch("src.utils.pd.read_excel")
    def test_get_top_transactions(mock_read_excel, mock_data, expected_result):
        mock_df = pd.DataFrame(mock_data)
        mock_read_excel.return_value = mock_df

        result = get_top_transactions("dummy_path.xlsx")
        assert result == expected_result


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
@patch("os.path.exists")
def test_load_json_success(mock_exists, mock_open_file):
    mock_exists.return_value = True

    result = load_json("test.json")
    assert result == {"key": "value"}


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open)
def test_load_json_file_not_found(mock_open_file, mock_exists):
    mock_exists.return_value = False

    result = load_json("nonexistent.json")
    assert result is None


@patch("src.main.requests.get")
def test_fetch_exchange_rates_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"conversion_rate": 70.5}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    dat = {"user_currencies": ["USD", "EUR"]}
    result = fetch_exchange_rates(dat)
    expected = [{"currency": "USD", "rate": 70.5}, {"currency": "EUR", "rate": 70.5}]
    assert result == expected


@patch("src.main.requests.get")
def test_fetch_exchange_rates_http_error(mock_get):
    mock_get.side_effect = requests.exceptions.HTTPError

    dat = {"user_currencies": ["USD"]}
    result = fetch_exchange_rates(dat)
    assert result == []


@patch("requests.get")
@patch("os.getenv")
def test_get_stocks_success(mock_getenv, mock_requests):
    mock_getenv.return_value = "test_api_key"
    mock_response = Mock()
    mock_response.json.return_value = [{"price": 123.45}]
    mock_response.raise_for_status = Mock()
    mock_requests.return_value = mock_response

    data = {"user_stocks": ["AAPL"]}
    result = get_stocks(data)

    assert result == [{"stock": "AAPL", "price": 123.45}]
    mock_requests.assert_called_once_with("https://financialmodelingprep.com/api/v3/quote/AAPL?apikey=test_api_key")


@patch("requests.get")
@patch("os.getenv")
def test_get_stocks_no_stocks(mock_getenv, mock_requests):
    mock_getenv.return_value = "test_api_key"
    data = {"user_stocks": []}
    result = get_stocks(data)

    assert result == []
    mock_requests.assert_not_called()


def test_filter_transactions_by_card():
    data = {
        "Номер карты": ["1234567890123456", "1234567890123456", "6543210987654321", "6543210987654321"],
        "Сумма платежа": [-100.50, -200.75, -50.25, -150.00],
        "Дата операции": ["01.12.2021 18:00:00", "02.12.2021 18:00:00", "03.12.2021 18:00:00", "04.12.2021 18:00:00"],
    }
    df_transactions = pd.DataFrame(data)

    expected_result = [
        {"last_digits": "3456", "total_spent": 301.25, "cashback": 3.01},
        {"last_digits": "4321", "total_spent": 200.25, "cashback": 2.00},
    ]

    # Вызов тестируемой функции
    result = filter_transactions_by_card(df_transactions, "17.12.2021 18:00:00")

    print("Результат:", result)
    print("Ожидаемый результат:", expected_result)

    # Проверка результата
    assert result == expected_result, f"Ожидалось {expected_result}, но получено {result}"


@pytest.mark.parametrize(
    "end_date, expected_length",
    [
        ("30.09.2021 23:59:59", 3),
        ("01.09.2021 12:00:00", 0),
        ("15.09.2021 12:00:00", 0),
        ("01.10.2021 12:00:00", 1),
        ("31.08.2021 23:59:59", 0),
    ],
)
def test_filter_transactions_by_date(end_date, expected_length):
    data = {
        "Дата операции": [
            "29.09.2021 14:30:00",
            "30.09.2021 10:00:00",
            "01.09.2021 08:00:00",
            "15.09.2021 15:45:00",
            "01.10.2021 12:00:00",
        ],
        "Сумма": [100, 200, 150, 300, 400],
    }

    dat1 = pd.DataFrame(data)

    result = filter_transactions_by_date(dat1, end_date)
    assert len(result) == expected_length
