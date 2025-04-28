"""LINE通知の共通部."""

import os
import time

import requests  # noqa: D100
from dotenv import load_dotenv
from icecream import ic  # type: ignore

# LINE Messaging APIエンドポイント.
url = "https://api.line.me/v2/bot/message/push"

ic.configureOutput(includeContext=True)
load_dotenv(override=True)

class LineNotifierBase:
    """LINE通知機能クラス."""
    def __init__(self, debug_config: dict, token: str, to_channel_id: str):
        """LineNotifierBase のインスタンスを初期化.

        Args:
            debug_config (dict): デバッグ設定を含む辞書.
            - 'is_debug_to_line' (bool): True=ログ出力, False=LINEに通知
            - 'is_debug_target_id' (bool): True=個人ユーザ, False=本番用チャンネル
            token (str): LINE APIの認証トークン。
            to_channel_id (str): メッセージ送信先のチャンネルID（本番環境用）。
        """
        self.token = token
        self.debug_config = debug_config

        if debug_config.get("is_debug_target_id", True):
            self.to_channel_id = os.getenv("LINE_USER_ID")
        else:
            self.to_channel_id = to_channel_id

    def notify(self, msg: str):
        """メッセージ送信."""
        # ヘッダー設定
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {
            "to": self.to_channel_id,
            "messages": msg
        }

        if self.debug_config.get("is_debug_to_line", True):
            ic(f"【DEBUG】メッセージが送信されました.: {msg}")
        else:
            # メッセージ送信
            response = requests.post(url, headers=headers, json=payload)

            # ステータスを確認
            if response.status_code == 200:
                ic(f"メッセージが送信されました.: {msg}")
            else:
                ic(f"エラーが発生しました.: {response.status_code}, {response.text}")

    @staticmethod
    def add_timestamp_to_url(url):
        """timestampありURLへ更新."""
        timestamp = int(time.time())
        return f"{url}?ts={timestamp}"
