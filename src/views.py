import json
import math
import os
from datetime import datetime
from typing import Any, Hashable

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame


def get_greeting(current_time: Any) -> str:
    if 5 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def process_card(card_info: Any) -> dict:
    card_number = card_info["MCC"]
    expenses = card_info["Сумма операции с округлением"]
    if math.isnan(card_number):
        last_digits = None
    else:
        last_digits = int(card_number)
    total_spent = expenses
    cashback = total_spent // 100
    return {"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback}


def get_top_transactions(transactions: Any) -> list[Any]:
    # Сортируем транзакции по сумме и выбираем топ 5
    top_transactions = transactions.sort_values(by="Сумма операции с округлением", ascending=False).head(5)
    return (
        top_transactions[["Дата операции", "Сумма операции с округлением", "Категория", "Описание"]]
        .rename(
            columns={
                "Дата операции": "date",
                "Сумма операции с округлением": "amount",
                "Категория": "category",
                "Описание": "description",
            }
        )
        .to_dict(orient="records")
    )


def filter_transactions_by_date(top_transactions: Any, end_date) -> list[Any]:
    # Фильтруем транзакции с 1 числа каждого месяца по указанную дату
    start_date = datetime(end_date.year, end_date.month, 1)
    filtered_transactions = top_transactions[
        (top_transactions["Дата операции"] >= start_date) & (top_transactions["Дата операции"] <= end_date)
    ]
    return filtered_transactions


def main(date_time_input: str, card_data: str, transactions_data: DataFrame) -> str:
    # Проверяем тип datetimeinput
    if isinstance(date_time_input, str):
        current_time = datetime.strptime(date_time_input, "%d.%m.%Y %H:%M:%S")
    else:
        current_time = date_time_input  # Если это уже Timestamp, используем его

    # Получаем приветствие
    greeting = get_greeting(current_time)

    # Обрабатываем карты
    cards_info = [process_card(card) for card in card_data]

    # Фильтруем транзакции
    end_date = current_time
    top_transactions = get_top_transactions(transactions_data)
    filtered_transactions = filter_transactions_by_date(top_transactions, end_date)

    for transaction in top_transactions:
        transaction["date"] = transaction["date"].strftime("%d.%m.%Y %H:%M:%S")

    # Формируем JSON-ответ
    response = {"greeting": greeting, "cards": cards_info, "filtered_transactions": filtered_transactions}

    return json.dumps(response, ensure_ascii=False)


def load_data_from_excel(file_xlsx: str) -> pd.DataFrame:
    # Загружаем данные из файла Excel
    df = pd.read_excel(file_xlsx)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    return df


file_xlsx = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
df = load_data_from_excel(file_xlsx)

date_time_input = df["Дата операции"].iloc[0]  # Берём первую строку для примера
card_data_input = df[["MCC", "Сумма операции с округлением"]].to_dict(orient="records")
transactions_data_input = df[["Дата операции", "Сумма операции с округлением", "Категория", "Описание"]]

# Преобразуем расходы из строкового формата в списки
for card in card_data_input:
    card["Сумма операции с округлением"] = float(card["Сумма операции с округлением"])


result = main(date_time_input, card_data_input, transactions_data_input)
print(result)
