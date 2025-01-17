import json
from unittest.mock import patch

import pandas as pd

from src.reports import save_to_file_decorator, spending_by_category


def test_save_to_file_decorator(tmp_path):
    # tmp_path — это временная директория, предоставляемая pytest
    test_file = tmp_path / "test_log.json"
    with patch("src.reports.logger") as mock_logger:

        @save_to_file_decorator(test_file)
        def test_function() -> pd.DataFrame:
            data = {
                "Дата операции": ["15.02.2023", "20.03.2023"],
                "Сумма операции": [2000, 3000],
            }
            return pd.DataFrame(data)

        result = test_function()
        assert isinstance(result, pd.DataFrame)
        assert test_file.exists()
        with open(test_file, "r", encoding="utf-8") as file:
            file_data = json.load(file)

        expected_data = [
            {"Дата операции": "15.02.2023", "Сумма операции": 2000},
            {"Дата операции": "20.03.2023", "Сумма операции": 3000},
        ]
        assert file_data == expected_data

        mock_logger.info.assert_any_call("Декоратор записывает полученный результат в файл.")
        mock_logger.info.assert_any_call("Декоратор успешно завершил свою работу.")


def test_spending_by_category():
    # Создаем тестовый DataFrame с транзакциями
    data = {
        "Дата операции": [
            "15.02.2023 14:30:00",
            "20.03.2023 18:00:00",
            "01.04.2023 12:00:00",
            "01.01.2023 10:00:00",
            "01.05.2023 12:00:00",
        ],
        "Сумма операции с округлением": [2000, 3000, 500, 1500, 1000],
        "Категория": ["Развлечения", "Супермаркеты", "Супермаркеты", "Развлечения", "Косметика"],
    }
    df_transactions = pd.DataFrame(data)

    # Устанавливаем дату для проверки
    test_date = "01.05.2023 00:00:00"

    # Ожидаемый результат
    expected_result = [
        {"Дата операции": "20.03.2023 18:00:00", "Сумма операции с округлением": 3000, "Категория": "Супермаркеты"},
        {"Дата операции": "01.04.2023 12:00:00", "Сумма операции с округлением": 500, "Категория": "Супермаркеты"},
    ]

    # Вызываем функцию
    result = spending_by_category(df_transactions, category="Супермаркеты", date=test_date)

    # Проверяем, что результат совпадает с ожидаемым
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
