import pytest
import pandas as pd
from datetime import datetime
from src.reports import spending_by_category


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
