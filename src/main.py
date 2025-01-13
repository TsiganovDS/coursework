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
        while True:
            user_input = input(f"{sp}1.Поиск переводов физическим лицам \n{sp}2. По переводам на мобильные номера\n{sp}Номер : ")

            if user_input == "1":
                print(transfers_to_individuals(df_transactions))
                break
            elif user_input == "2":
                print(transfers_to_phone(df_transactions))
                break

    def action_3() -> None:
        user_input = input(f"\n{sp}1.Супермаркеты \n{sp}2. Каршеринг \n{sp}3. Развлечения\n{sp}4.Фастфуд \n{sp}5. Связь \n{sp}6.Местный транспорт \n{sp}7.Косметика\n{sp}Выберите категорию: ")

        if user_input == "1":
            category = "Супермаркеты"
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59").to_dict("records")
                print(data_dict)

        elif user_input == "2":
            category = "Каршеринг"
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59").to_dict("records")
                print(data_dict)

        elif user_input == "3":
            category = "Развлечения"
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59").to_dict("records")
                print(data_dict)

        elif user_input == "4":
            category = "Фастфуд"
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59").to_dict("records")
                print(data_dict)

        elif user_input == "5":
            category = "Связь"
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59").to_dict("records")
                print(data_dict)

        elif user_input == "6":
            category = "Местный транспорт"
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59").to_dict("records")
                print(data_dict)

        elif user_input == "7":
            category = "Косметика"
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59").to_dict("records")
                print(data_dict)



    print("*" * 30 + " SKY BANK " + "*" * 30)
    print(" " * 9 + "Внимание!!! Для отчета используется дата: 31.12.2021")
    user_input = input(f"{sp}1.Главная страница\n{sp}2.Сервисы\n{sp}3.Отчеты\n{sp}Номер: ")
    while True:
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
