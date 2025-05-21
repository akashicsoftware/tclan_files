import os
import time
import pytest
from unittest.mock import patch, MagicMock

from line_notifier_base import LineNotifierBase  # ファイル名に応じて変更してください


@pytest.fixture
def dummy_env(monkeypatch):
    """
    環境変数をテスト用のダミー値で上書きする。
    """
    monkeypatch.setenv("LINE_USER_ID", "dummy_user_id")


def test_init_sets_to_channel_id_based_on_debug_flag(dummy_env):
    """
    LineNotifierBase のコンストラクタが debug_config に応じて
    to_channel_id を環境変数か引数から正しくセットするかを検証する。

    - is_debug_target_id True のときは環境変数LINE_USER_IDを使う
    - False のときはコンストラクタ引数のチャンネルIDを使う
    """
    debug_config = {"is_debug_target_id": True}
    notifier = LineNotifierBase(debug_config, "dummy_token", "dummy_channel_id")
    assert notifier.to_channel_id == "dummy_user_id"

    debug_config = {"is_debug_target_id": False}
    notifier = LineNotifierBase(debug_config, "dummy_token", "dummy_channel_id")
    assert notifier.to_channel_id == "dummy_channel_id"


@patch("line_notifier_base.ic")
def test_notify_logs_message_in_debug_mode(mock_ic, dummy_env):
    """
    notify() が is_debug_to_line=True のときは
    実際の送信は行わず、ic()でログ出力することを検証する。

    - ic()が一度呼ばれる
    - 送信メッセージがログに含まれる
    """
    debug_config = {"is_debug_to_line": True, "is_debug_target_id": True}
    notifier = LineNotifierBase(debug_config, "dummy_token", "dummy_channel_id")
    notifier.notify("debug test message")

    mock_ic.assert_called_once()
    args, _ = mock_ic.call_args
    assert "debug test message" in args[0]


@patch("line_notifier_base.requests.post")
@patch("line_notifier_base.ic")
def test_notify_sends_message_and_logs_success(mock_ic, mock_post):
    """
    notify() が is_debug_to_line=False のとき、
    requests.post() が呼ばれ、ステータス200なら成功ログが出ることを検証する。

    - requests.post() が一度呼ばれる
    - ic() で成功メッセージが出力される
    """
    debug_config = {"is_debug_to_line": False, "is_debug_target_id": False}
    notifier = LineNotifierBase(debug_config, "dummy_token", "dummy_channel_id")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "OK"
    mock_post.return_value = mock_response

    notifier.notify("send success")

    mock_post.assert_called_once()
    mock_ic.assert_called_once()
    args, _ = mock_ic.call_args
    assert "send success" in args[0]


@patch("line_notifier_base.requests.post")
@patch("line_notifier_base.ic")
def test_notify_sends_message_and_logs_error(mock_ic, mock_post):
    """
    notify() が is_debug_to_line=False のとき、
    requests.post() が呼ばれ、ステータスが200以外ならエラーログが出ることを検証する。

    - requests.post() が一度呼ばれる
    - ic() でエラーメッセージが出力される
    """
    debug_config = {"is_debug_to_line": False, "is_debug_target_id": False}
    notifier = LineNotifierBase(debug_config, "dummy_token", "dummy_channel_id")

    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_post.return_value = mock_response

    notifier.notify("send failure")

    mock_post.assert_called_once()
    mock_ic.assert_called_once()
    args, _ = mock_ic.call_args
    assert "エラー" in args[0]
    assert "400" in args[0]
    assert "Bad Request" in args[0]


def test_add_timestamp_to_url_returns_url_with_timestamp():
    """
    add_timestamp_to_url() が与えられたURLに
    現在時刻のタイムスタンプをクエリパラメータとして付与して返すことを確認する。

    - 元のURLに'?ts='で始まるパラメータが付く
    - タイムスタンプは現在時刻の範囲内である
    """
    url = "https://example.com/path"
    before = int(time.time())
    result = LineNotifierBase.add_timestamp_to_url(url)
    after = int(time.time())

    assert result.startswith(url + "?ts=")
    ts = int(result.split("ts=")[1])
    assert before <= ts <= after
