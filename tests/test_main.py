from unittest.mock import patch

import pandas as pd

from src.main import main

mock_df = pd.DataFrame(
    {
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
)


@patch("src.reports.spending_by_category", return_value=mock_df)
@patch("builtins.input", side_effect=["3", "1"])
@patch("builtins.print")
def test_main(mock_print, mock_input, mock_load_data):
    main()

    mock_print.assert_any_call("*" * 30 + " SKY BANK " + "*" * 30)
    mock_print.assert_any_call(" " * 9 + "Внимание!!! Для отчета используется дата: 31.12.2021")
