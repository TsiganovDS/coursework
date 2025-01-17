import json

import pandas as pd


def test_transfers_to_individuals():
    transactions = pd.DataFrame(
        [
            {"Категория": "Переводы", "Описание": "Иван И."},
            {"Категория": "Продукты", "Описание": "Магазин"},
            {"Категория": "Переводы", "Описание": "Петр П."},
            {"Категория": "Прочее", "Описание": "Пример"},
        ]
    )

    expected_result = json.dumps(
        [{"Категория": "Переводы", "Описание": "Иван И."}, {"Категория": "Переводы", "Описание": "Петр П."}],
        ensure_ascii=False,
        indent=4,
    )

    from src.services import transfers_to_individuals

    result = transfers_to_individuals(transactions)
    assert result == expected_result


def test_transfers_to_phone() -> None:
    data = {
        "Описание": [
            "Перевод на номер +7 123 456-00-00",
            "Оплата услуги",
            "Перевод на номер +8 987 654-45-45",
            "Транзакция без номера",
            "Перевод на номер +7 777 777-88-00",
        ],
        "Сумма": [100, 200, 150, 300, 250],
    }
    df = pd.DataFrame(data)

    expected_result = [
        {"Описание": "Перевод на номер +7 123 456-00-00", "Сумма": 100},
        {"Описание": "Перевод на номер +8 987 654-45-45", "Сумма": 150},
        {"Описание": "Перевод на номер +7 777 777-88-00", "Сумма": 250},
    ]

    from src.services import transfers_to_phone

    result = transfers_to_phone(df)
    result_data = json.loads(result)
    assert result_data == expected_result, f"Expected {expected_result}, but got {result_data}"
