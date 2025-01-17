import datetime as dt
import json
import os
from datetime import datetime
from typing import Any, Optional

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

from src.logger import setting_logger

logger = setting_logger("utils")


file_xlsx = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
file_log = os.path.join(os.path.dirname(__file__), "..", "logs", "log_file.json")
file_json = os.path.join(os.path.dirname(__file__), "..", "data", "user_setting.json")


def load_data_from_excel(file_xlsx: str) -> pd.DataFrame | None:
    """Функция преобразования Excel-файла в DataFrame"""
    try:
        df = pd.read_excel(file_xlsx)
    except FileNotFoundError:
        logger.warning(f"Файл не найден: {file_xlsx}")
        raise
    except pd.errors.ParserError:
        logger.warning("Ошибка чтения файла")
        raise

    logger.info("Файл успешно открыт")
    return df


def get_greeting() -> str:
    """Функция, возращает приветствие в зависимости от текущего времени"""
    current_time = dt.datetime.now().hour
    logger.info("Функция get_greeting начала свою работу.")
    if 5 <= current_time < 12:
        logger.info("Функция get_greeting успешно завершила свою работу.")
        return "Доброе утро"
    elif 12 <= current_time < 18:
        logger.info("Функция get_greeting успешно завершила свою работу.")
        return "Добрый день"
    elif 18 <= current_time < 23:
        logger.info("Функция get_greeting успешно завершила свою работу.")
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_top_transactions(transactions: pd.DataFrame) -> list[dict] | None:
    """Функция, принимает на вход DataFrame транзакций и
    возвращает список словарей с ТОП-5 транзакций по сумме платежа."""
    logger.info("Функция get_top_transactions начала свою работу.")
    try:
        df = pd.read_excel(file_xlsx)

        required_columns = ["Дата платежа", "Сумма операции", "Категория", "Описание"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Отсутствуют необходимые столбцы в данных")

        transactions = df[required_columns].copy()
        transactions["Сумма операции"] = transactions["Сумма операции"].astype(float)

        top_5_transactions = transactions.nlargest(5, "Сумма операции")

        result = [
            {
                "date": (
                    row["Дата платежа"].strftime("%d.%m.%Y")
                    if isinstance(row["Дата платежа"], pd.Timestamp)
                    else str(row["Дата платежа"])
                ),
                "amount": round(row["Сумма операции"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
            for index, row in top_5_transactions.iterrows()
        ]
        logger.info("Функция get_top_transactions успешно завершила свою работу.")
        return result

    except Exception as e:
        logger.info(f"Произошла ошибка: {e}")
        return []


def load_json(file_json: str) -> dict[str, Any] | None:
    logger.info("Функция load_json начала свою работу")
    if not os.path.exists(file_json):
        logger.warning(f"Файл не найден: {file_json}")
        return None
    try:
        with open(file_json, "r", encoding="utf-8") as file:
            dat = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        logger.warning("Ошибка чтения json-файла")
        return None
    logger.info("Функция load_json успешно завершила свою работу.")
    return dat


dat = load_json(file_json)


load_dotenv(".env")
API_KEY = os.getenv("API_KEY")


def fetch_exchange_rates(dat: dict) -> dict[Any, Any] | list[Any]:
    """Функция курса валют, формирует словари по ключу currency_rates"""
    logger.info("Функция fetch_exchange_rates начала свою работу")
    want_rub = "RUB"
    currency_rates = []
    for currency in dat["user_currencies"]:
        try:
            response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{currency}/{want_rub}")
            if response.status_code == 200:
                rate = response.json().get("conversion_rate", None)
                currency_rates.append({"currency": currency, "rate": rate})
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")  # Логируем ошибку
        except Exception as e:
            print(f"An error occurred: {e}")
    logger.info("Функция fetch_exchange_rates успешно завершила свою работу.")
    return currency_rates


def get_stocks(dat: dict) -> list[dict] | None:
    """Функция стоимости акций, формирует словари по ключу stock_prices"""
    logger.info("Функция get_stocks начала свою работу")
    stocks = dat.get("user_stocks")
    apikey = os.getenv("API_KEY_STOCK")
    stocks_prices = []

    if not stocks:
        logger.warning("Нет акций для получения цен.")
        return []

    try:
        for stock in stocks:
            url = f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={apikey}"
            response = requests.get(url)
            response.raise_for_status()  # Выбрасывает исключение для плохих ответов
            result = response.json()
            if result:
                stock_price = {"stock": stock, "price": result[0]["price"]}
                stocks_prices.append(stock_price)
            else:
                logger.warning(f"Нет данных для акции: {stock}")
        logger.info("Функция get_stocks успешно завершила свою работу.")
        return stocks_prices
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API запроса: {e}")
        return None


def filter_transactions_by_card(df_transactions: pd.DataFrame) -> list[dict]:
    """Функция принимает DataFrame с транзакциями
    и возвращает общую информацию по каждой карте"""
    logger.info("Функция filter_transactions_by_card начала свою работу.")
    cards_dict = (
        df_transactions.loc[df_transactions["Сумма платежа"] < 0]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )
    expenses_cards = []
    for card, expenses in cards_dict.items():
        expenses_cards.append(
            {
                "last_digits": card[-4:],
                "total_spent": abs(round(expenses, 2)),
                "cashback": abs(round(expenses / 100, 2)),
            }
        )
    logger.info("Функция filter_transactions_by_card успешно завершила свою работу.")
    return expenses_cards


def filter_transactions_by_date(transactions_df: pd.DataFrame, end_date: Optional[str]) -> DataFrame:
    """Функция, фильтрации транзакций по дате.Формат даты: %d.%m.%Y %H:%M:%S"""
    logger.info("Функция filter_transactions_by_date начала свою работу.")
    transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    end_date = pd.to_datetime(end_date, format="%d.%m.%Y %H:%M:%S")
    filtered_transactions = transactions_df[transactions_df["Дата операции"] <= end_date]
    logger.info("Функция filter_transactions_by_date успешно завершила свою работу.")
    return filtered_transactions
