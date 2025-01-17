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
            user_input = input(
                f"{sp}1. Поиск переводов физическим лицам \n{sp}2. По переводам на мобильные номера\n{sp}Номер : "
            )
            if user_input in ["1", "2"]:
                print(
                    transfers_to_individuals(df_transactions)
                    if user_input == "1"
                    else transfers_to_phone(df_transactions)
                )
                break

    def action_3() -> None:
        user_input = input(
            f"\n{sp}1. Супермаркеты \n{sp}2. Каршеринг \n{sp}3. Развлечения\n{sp}4. Фастфуд \n{sp}5. Связь \n{sp}"
            f"6. Местный транспорт \n{sp}7. Косметика\n{sp}8. Сувениры\n{sp}9. Аптеки\n{sp}Выберите категорию: "
        )

        categories = {
            "1": "Супермаркеты",
            "2": "Каршеринг",
            "3": "Развлечения",
            "4": "Фастфуд",
            "5": "Связь",
            "6": "Местный транспорт",
            "7": "Косметика",
            "8": "Сувениры",
            "9": "Аптеки",
        }

        if user_input in categories:
            category = categories[user_input]
            if category in df_transactions["Категория"].values:
                data_dict = spending_by_category(df_transactions, category, "31.12.2021 23:59:59")
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
