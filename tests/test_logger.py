import logging
import os
import unittest

from src.logger import setting_logger

file_l = os.path.join(os.path.dirname(__file__), "..", "logs", "logfile.log")


def test_setting_logger(caplog):
    test_message = "Здравствуйте"
    with caplog.at_level(logging.INFO):
        setting_logger(test_message)

    assert len(caplog.records) == 1
    assert caplog.records[0].message == test_message
    assert caplog.records[0].levelname == "INFO"
