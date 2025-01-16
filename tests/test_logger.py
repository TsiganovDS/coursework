import logging

import pytest

from src.logger import setting_logger

def test_setting_logger(caplog):
    test_message = "Доброй ночи"

    with caplog.at_level(logging.INFO):
        setting_logger(test_message)

    # Проверяем, что логгер записал нужное сообщение
    assert len(caplog.records) == 1  # Проверка, что записано одно сообщение
    assert caplog.records[0].message == test_message  # Проверка содержимого сообщения
    assert caplog.records[0].levelname == "INFO"