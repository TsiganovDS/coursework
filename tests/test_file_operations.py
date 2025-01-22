import os
import unittest
from os import name
from unittest.mock import patch

import pandas as pd

from src.logger import setting_logger
from src.utils import load_data_from_excel

logger = setting_logger("test_file_operations")


class TestFileOperations(unittest.TestCase):
    @patch("src.utils.logger")
    def test_file_not_found(self, mock_logger):
        file_xls = os.path.join(os.path.dirname(__file__), "..", "data", "non_existent_file.xlsx")

        with self.assertRaises(FileNotFoundError):
            load_data_from_excel(file_xls)

        mock_logger.warning.assert_called_once_with(f"Файл не найден: {file_xls}")

    @patch("src.utils.logger")
    @patch("pandas.read_excel", side_effect=pd.errors.ParserError)
    def test_parser_error(self, mock_read_excel, mock_logger):
        file_xls = os.path.join(os.path.dirname(__file__), "..", "data", "some_file.xlsx")

        with self.assertRaises(pd.errors.ParserError):
            load_data_from_excel(file_xls)

        mock_logger.warning.assert_called_once_with("Ошибка чтения файла")


if name == "main":
    unittest.main()
