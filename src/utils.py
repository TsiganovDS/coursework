import datetime as dt
import json
import os
from typing import Any, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

from src.logger import setting_logger

logger = setting_logger("utils")


file_xlsx = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
file_log = os.path.join(os.path.dirname(__file__), "..", "logs", "log_file.json")
file_json = os.path.join(os.path.dirname(__file__), "..", "user_setting.json")


def load_data_from_excel(file_xlsx: str) -> pd.DataFrame | None:
    """Функция преобразования Excel-файла в DataFrame"""
    logger.info("Функция начала свою работу.")
    try:
        df = pd.read_excel(file_xlsx)
    except FileNotFoundError:
        logger.warning(f"Файл не найден: {file_xlsx}")
        raise
    except pd.errors.ParserError:
        logger.warning("Ошибка чтения файла")
        raise

    logger.info("Файл успешно открыт")
    logger.info("Функция успешно завершила свою работу.")
    return df


def get_greeting() -> str:
    """Функция, возращает приветствие в зависимости от текущего времени"""
    current_time = dt.datetime.now().hour
    logger.info("Функция начала свою работу.")
    if 5 <= current_time < 12:
        logger.info("Функция успешно завершила свою работу.")
        return "Доброе утро"
    elif 12 <= current_time < 18:
        logger.info("Функция успешно завершила свою работу.")
        return "Добрый день"
    elif 18 <= current_time < 23:
        logger.info("Функция успешно завершила свою работу.")
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_json(file_json: str) -> Any:
    logger.info("Функция начала свою работу")
    if not os.path.exists(file_json):
        logger.warning(f"Файл не найден: {file_json}")
        return None
    try:
        with open(file_json, "r", encoding="utf-8") as file:
            dat = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        logger.warning("Ошибка чтения json-файла")
        return None
    logger.info("Функция успешно завершила свою работу.")
    return dat


dat = load_json(file_json)


load_dotenv(".env")
API_KEY = os.getenv("API_KEY")


def fetch_exchange_rates(dat: dict) -> dict[Any, Any] | list[Any]:
    """Функция курса валют, формирует словари по ключу currency_rates"""
    logger.info("Функция начала свою работу")
    want_rub = "RUB"
    currency_rates = []
    load_dotenv()
    apikey = os.getenv("API_KEY")
    for currency in dat["user_currencies"]:
        try:
            response = requests.get(f"https://v6.exchangerate-api.com/v6/{apikey}/pair/{currency}/{want_rub}")
            if response.status_code == 200:
                rate = response.json().get("conversion_rate", None)
                rate = round(rate, 2)
                currency_rates.append({"currency": currency, "rate": rate})
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")  # Логируем ошибку
        except Exception as e:
            print(f"An error occurred: {e}")
    logger.info("Функция успешно завершила свою работу.")
    return currency_rates


def get_stocks(dat: dict) -> list[dict] | None:
    """Функция стоимости акций, формирует словари по ключу stock_prices"""
    logger.info("Функция начала свою работу")
    stocks = dat.get("user_stocks")
    load_dotenv(".env")
    apikey = os.getenv("API_KEY_STOCK")
    stocks_prices = []

    if not stocks:
        logger.warning("Нет акций для получения цен.")
        return []

    try:
        for stock in stocks:
            url = f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={apikey}"
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            if result:
                stock_price = {"stock": stock, "price": result[0]["price"]}
                stocks_prices.append(stock_price)
            else:
                logger.warning(f"Нет данных для акции: {stock}")
        logger.info("Функция успешно завершила свою работу.")
        return stocks_prices
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API запроса: {e}")
        return None


def get_top_transactions(transactions: pd.DataFrame) -> list[dict] | None:
    """Функция, принимает на вход DataFrame транзакций и
    возвращает список словарей с ТОП-5 транзакций по сумме платежа."""
    logger.info("Функция начала свою работу.")
    try:
        df = pd.read_excel(file_xlsx)

        required_columns = ["Дата операции", "Сумма операции", "Категория", "Описание"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Отсутствуют необходимые столбцы в данных")
        transactions = df[required_columns].copy()
        transactions["Сумма операции"] = transactions["Сумма операции"].astype(float)
        trans = filter_transactions_by_date(transactions, "31.12.2021 00:00:00")
        if trans.empty:
            logger.info("Нет доступных транзакций для анализа.")
            return None
        top_5_transactions = trans.nlargest(5, "Сумма операции")

        result = [
            {
                "date": (
                    row["Дата операции"].strftime("%d.%m.%Y")
                    if isinstance(row["Дата операции"], pd.Timestamp)
                    else str(row["Дата операции"])
                ),
                "amount": round(row["Сумма операции"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
            for index, row in top_5_transactions.iterrows()
        ]
        logger.info("Функция успешно завершила свою работу.")
        return result

    except Exception as e:
        logger.info(f"Произошла ошибка: {e}")
        return None


def filter_transactions_by_card(df_transactions: pd.DataFrame, end_date) -> list[dict]:
    """Функция принимает DataFrame с транзакциями
    и возврщает общую информацию по каждой карте"""
    logger.info("Функция начала свою работу.")
    transactions = filter_transactions_by_date(df_transactions, end_date)
    cards_dict = (
        transactions.loc[transactions["Сумма платежа"] < 0]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )
    logger.info("Функция обрабатывает данные транзакций.")
    expenses_cards = []
    for card, expenses in cards_dict.items():
        expenses_cards.append(
            {
                "last_digits": card[-4:],
                "total_spent": abs(round(expenses, 2)),
                "cashback": abs(round(expenses / 100, 2)),
            }
        )
    logger.info("Функция успешно завершила свою работу.")
    return expenses_cards


def filter_transactions_by_date(df_transactions: pd.DataFrame, end_date: Optional[str]) -> pd.DataFrame:
    """Функция фильтрации и сортировки транзакций по дате. Формат даты: %d.%m.%Y %H:%M:%S"""
    logger.info("Функция начала свою работу.")

    df_transactions["Дата операции"] = pd.to_datetime(df_transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    end_date = pd.to_datetime(end_date, format="%d.%m.%Y %H:%M:%S")

    start_date = end_date.replace(day=1)

    filtered_transactions = df_transactions[
        (df_transactions["Дата операции"] >= start_date) & (df_transactions["Дата операции"] <= end_date)
    ]

    filtered_transactions = filtered_transactions.sort_values(by="Дата операции")

    logger.info("Функция успешно завершила свою работу.")
    return filtered_transactions
