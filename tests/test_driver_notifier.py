import os
import pytest
from unittest.mock import patch
from datetime import datetime

from driver_notifier import DriverNotifier, user_pdf_url


@pytest.fixture
def dummy_env(monkeypatch):
    """環境変数をテスト用にモック"""
    monkeypatch.setenv("LINE_API_TOKEN", "dummy_token")
    monkeypatch.setenv("LINE_USER_ID", "dummy_user_id")
    monkeypatch.setenv("LINE_GROUP_ID_DRIVER_CHANNEL", "dummy_group_id")


def test_create_msg_with_matching_date_returns_driver_message(dummy_env):
    """
    create_msg()が debug_config の is_debug_date=True によって固定日付 2025-04-28 を使用し、
    対応するドライバー「澤」の送迎メッセージを返すかを確認。
    """
    debug_config = {
        "is_debug_date": True,
        "is_debug_to_line": True,
        "is_debug_target_id": True,
    }
    notifier = DriverNotifier(debug_config, "dummy_token", "dummy_channel_id")
    messages = notifier.create_msg()

    assert isinstance(messages, list)
    assert messages[0]["type"] == "template"
    assert "澤" in messages[0]["template"]["text"]
    assert messages[0]["template"]["actions"][0]["type"] == "uri"
    assert messages[0]["template"]["actions"][0]["uri"].startswith(user_pdf_url)


@patch("driver_notifier.datetime")
def test_create_msg_with_non_matching_today_returns_default_message(mock_datetime, dummy_env):
    """
    datetime.today() をモックしてどの範囲にもマッチしない日付を返すテスト。
    """
    mock_datetime.today.return_value = datetime(2025, 1, 1)
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)  # datetime(2025,4,28) の生成も有効にするため

    debug_config = {
        "is_debug_date": False,
        "is_debug_to_line": True,
        "is_debug_target_id": True,
    }
    notifier = DriverNotifier(debug_config, "dummy_token", "dummy_channel_id")
    messages = notifier.create_msg()

    assert isinstance(messages, list)
    assert messages[0]["type"] == "text"
    assert "送迎設定が行われていません" in messages[0]["text"]



@patch("driver_notifier.LineNotifierBase.notify")
def test_notify_called(mock_notify, dummy_env):
    """
    notify() メソッドが親クラスの notify を呼び出していることを確認。
    """
    debug_config = {
        "is_debug_date": True,
        "is_debug_to_line": True,
        "is_debug_target_id": True,
    }
    notifier = DriverNotifier(debug_config, "dummy_token", "dummy_channel_id")
    messages = notifier.create_msg()
    notifier.notify(messages)

    mock_notify.assert_called_once_with(messages)
