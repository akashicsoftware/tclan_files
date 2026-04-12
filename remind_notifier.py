"""出欠回答メッセージを通知する."""

import os
import textwrap

from dotenv import load_dotenv  # type: ignore
from icecream import ic  # type: ignore

from line_notifier_base import LineNotifierBase

ic.configureOutput(includeContext=True)
load_dotenv(override=True)

debug_config = {
    "is_debug_to_line": False,  # True=ログ出力, False=LINEに通知
    "is_debug_target_id": False,  # True=個人ユーザ, False=本番用チャンネル
}

# グラウンド場所のURL
spot_info_url = "https://sites.google.com/view/tclan/home/location"
# 年間スケジュールのPDF
scr_pdf_url = "https://akashicsoftware.github.io/tclan_files/external_files/scr.pdf"
# 年間スケジュールのgoogle カレンダー
scr_info_url = "https://sites.google.com/view/tclan/home/scr"

class RemindNotifier(LineNotifierBase):
    """出欠回答メッセージクラス."""
    def __init__(self, debug_config: dict, token: str, to_channel_id: str):
        """インスタンスを初期化.

        Args:
            debug_config (dict): デバッグ設定を含む辞書.
            - 'is_debug_to_line' (bool): True=ログ出力, False=LINEに通知
            - 'is_debug_target_id' (bool): True=個人ユーザ, False=本番用チャンネル
            token (str): LINE APIの認証トークン。
            to_channel_id (str): メッセージ送信先のチャンネルID（本番環境用）。
        """
        super().__init__(debug_config, token, to_channel_id)


    def create_msg(self):
        """メッセージ作成."""
        msg = textwrap.dedent("""\
            出欠回答が未の方は、本日中に回答お願いします。
            明日以降変更がある場合は、直接LINEに記載してください。
            """)
        payload_messages = [
            {
                "type": "template",
                "altText": msg,
                "template": {
                    "type": "buttons",
                    "text": msg,
                    "actions": [
                        {
                            "type": "uri",
                            "label": "🧭グラウンドの場所",
                            "uri": RemindNotifier.add_timestamp_to_url(spot_info_url)
                        },
                        {
                            "type": "uri",
                            "label": "📅年間予定",
                            "uri": RemindNotifier.add_timestamp_to_url(scr_pdf_url)
                        },
                        {
                            "type": "uri",
                            "label": "Google カレンダー",
                            "uri": RemindNotifier.add_timestamp_to_url(scr_info_url)
                        }
                    ]
                }
            }
        ]

        return payload_messages

if __name__ == "__main__":
    if debug_config.get("is_debug_target_id", True):
        to_channel_id = os.getenv("LINE_USER_ID")
    else:
        to_channel_id = os.getenv("LINE_GROUP_ID_MAIN_CHANNEL")
    notifier = RemindNotifier(debug_config, os.getenv('LINE_API_TOKEN'), to_channel_id)
    notifier.notify(notifier.create_msg())
