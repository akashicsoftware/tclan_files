import os
import pytest
from unittest.mock import patch, MagicMock

from remind_notifier import RemindNotifier, scr_pdf_url, location_info_url


@pytest.fixture
def dummy_env(monkeypatch):
    """
    環境変数をテスト用のダミー値で上書きする。
    """
    monkeypatch.setenv("LINE_API_TOKEN", "dummy_token")
    monkeypatch.setenv("LINE_USER_ID", "dummy_user_id")
    monkeypatch.setenv("LINE_GROUP_ID_MAIN_CHANNEL", "dummy_group_id")


def test_create_msg_returns_expected_structure(dummy_env):
    """
    RemindNotifier.create_msg() が正しい構造のLINEメッセージ（辞書のリスト）を返すかを確認する。

    - 返されるメッセージがリストである
    - "template" タイプである
    - altText, actionsなど必要なフィールドが正しく含まれている
    - リンクが正しく付加されている
    """
    debug_config = {"is_debug_to_line": True, "is_debug_target_id": True}
    notifier = RemindNotifier(debug_config, "dummy_token", "dummy_channel_id")

    messages = notifier.create_msg()

    assert isinstance(messages, list)
    assert messages[0]["type"] == "template"
    assert "altText" in messages[0]

    template = messages[0]["template"]
    assert template["type"] == "buttons"
    assert "actions" in template
    actions = template["actions"]

    assert len(actions) == 2

    # 🧭グラウンドの場所
    assert actions[0]["type"] == "uri"
    assert actions[0]["label"] == "🧭グラウンドの場所"
    assert actions[0]["uri"].startswith(location_info_url)

    # 📅年間予定
    assert actions[1]["type"] == "uri"
    assert actions[1]["label"] == "📅年間予定"
    assert actions[1]["uri"].startswith(scr_pdf_url)


@patch("remind_notifier.LineNotifierBase.notify")
def test_notify_called(mock_notify, dummy_env):
    """
    RemindNotifier.notify() を呼び出すと、親クラスの notify() が呼び出されることを確認する。

    - create_msg() で生成したメッセージを渡したときに
      mockされた notify() が1度だけ呼ばれるかを検証する
    """
    debug_config = {"is_debug_to_line": True, "is_debug_target_id": True}
    notifier = RemindNotifier(debug_config, "dummy_token", "dummy_channel_id")

    messages = notifier.create_msg()
    notifier.notify(messages)

    mock_notify.assert_called_once_with(messages)
