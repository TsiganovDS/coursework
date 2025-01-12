from typing import Any

from src.reports import spending_by_category
from src.services import transfers_to_individuals, transfers_to_phone
from src.utils import file_xlsx, load_data_from_excel
from src.views import generator_json_data

sp = " " * 25
df_transactions = load_data_from_excel(file_xlsx)


def main() -> None:
    def action_1() -> Any:
        print(generator_json_data(df_transactions, "31.12.2021 23:59:59"))

    def action_2() -> Any:
        print(
            f"\n{sp}Выберите сервис:\n{sp}1. Поиск переводов физическим лицам \n{sp}"
            f"2. По переводам на мобильные номера"
        )
        while True:
            user_input = input()
            if user_input == "1":
                print(transfers_to_individuals(df_transactions))
                break
            elif user_input == "2":
                print(transfers_to_phone(df_transactions))
                break

    def action_3() -> None:
        while True:
            category = input("Введите категорию: ")
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59").to_dict("records")
                print(data_dict)
                break

    print("*" * 30 + " SKY BANK " + "*" * 30)
    print(" " * 9 + "Внимание!!! Для отчета используется дата: 31.12.2021")
    print(f"{sp}Выберите категорию:\n{sp}1. Главная страница\n{sp}2. Сервисы\n{sp}3. Отчеты")

    while True:
        user_input = input()
        if user_input == "1":
            action_1()
            break
        elif user_input == "2":
            action_2()
            break
        elif user_input == "3":
            action_3()
            break
        else:
            continue


if __name__ == "__main__":
    main()
