"""送迎メッセージを通知する."""
import os
import textwrap
from datetime import datetime

from dotenv import load_dotenv  # type: ignore
from icecream import ic  # type: ignore

from line_notifier_base import LineNotifierBase

ic.configureOutput(includeContext=True)
load_dotenv(override=True)

debug_config = {
    "is_debug_date": False,  # True=指定日での実行, False=実行日
    "is_debug_to_line": False,  # True=ログ出力, False=LINEに通知
    "is_debug_target_id": False,  # True=個人ユーザ, False=本番用チャンネル
}

# 担当者のPDF
user_pdf_url = "https://akashicsoftware.github.io/tclan_files/external_files/driver.pdf"
# 担当者マップ
user_mapping = [
    (datetime(2026,4,13), datetime(2026,4,19), "森"),
    (datetime(2026,4,20), datetime(2026,4,26), "若林"),
    (datetime(2026,4,27), datetime(2026,5,3), "宮下"),
    (datetime(2026,5,4), datetime(2026,5,10), "小野"),
    (datetime(2026,5,11), datetime(2026,5,17), "浅野"),
    (datetime(2026,5,18), datetime(2026,5,24), "澤"),
    (datetime(2026,5,25), datetime(2026,5,31), "坂野"),
    (datetime(2026,6,1), datetime(2026,6,7), "遠藤"),
    (datetime(2026,6,8), datetime(2026,6,14), "伏黒"),
    (datetime(2026,6,15), datetime(2026,6,21), "森"),
    (datetime(2026,6,22), datetime(2026,6,28), "若林"),
    (datetime(2026,6,29), datetime(2026,7,5), "宮下"),
    (datetime(2026,7,6), datetime(2026,7,12), "小野"),
    (datetime(2026,7,13), datetime(2026,7,19), "浅野"),
    (datetime(2026,7,20), datetime(2026,7,26), "澤"),
    (datetime(2026,7,27), datetime(2026,8,2), "坂野"),
    (datetime(2026,8,3), datetime(2026,8,9), "遠藤"),
    (datetime(2026,8,10), datetime(2026,8,16), "伏黒"),
    (datetime(2026,8,17), datetime(2026,8,23), "森"),
    (datetime(2026,8,24), datetime(2026,8,30), "若林"),
    (datetime(2026,8,31), datetime(2026,9,6), "宮下"),
    (datetime(2026,9,7), datetime(2026,9,13), "小野"),
    (datetime(2026,9,14), datetime(2026,9,20), "浅野"),
    (datetime(2026,9,21), datetime(2026,9,27), "澤"),
    (datetime(2026,9,28), datetime(2026,10,4), "坂野"),
    (datetime(2026,10,5), datetime(2026,10,11), "遠藤"),
    (datetime(2026,10,12), datetime(2026,10,18), "伏黒"),
    (datetime(2026,10,19), datetime(2026,10,25), "森"),
]

class DriverNotifier(LineNotifierBase):
    """送迎連絡クラス."""
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
        self.debug_config = debug_config


    def create_msg(self):
        """メッセージ作成."""
        # 実行日.
        if self.debug_config.get("is_debug_date", True):
            today = datetime(2026, 4, 28)
        else:
            today = datetime.today()

        # 範囲に基づいてメッセージを選択
        for date_range, target_user in [(r[:2], r[2]) for r in user_mapping]:
            if date_range[0] <= today <= date_range[1]:
                msg = textwrap.dedent(f"""\
                    今週の送迎は、 {target_user} さんです。
                    マネージャーの出欠状況を確認して、木曜日までに連絡してください。
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
                                    "label": "🚗当番表",
                                    "uri":
                                    DriverNotifier.add_timestamp_to_url(user_pdf_url)
                                }
                            ]
                        }
                    }
                ]
                break
        else:
            # 該当なしの場合のデフォルトメッセージ
            msg = textwrap.dedent("""\
                @m-asanuma
                今週の送迎設定が行われていません。送迎設定を行ってください。
                (変えて無ければ) github-Actionsで稼働しているはず。
                """)
            payload_messages = [{"type": "text", "text": msg}]

        return payload_messages

if __name__ == "__main__":
    if debug_config.get("is_debug_target_id", True):
        to_channel_id = os.getenv("LINE_USER_ID")
    else:
        to_channel_id = os.getenv("LINE_GROUP_ID_DRIVER_CHANNEL")
    notifier = DriverNotifier(debug_config, os.getenv('LINE_API_TOKEN'), to_channel_id)
    notifier.notify(notifier.create_msg())
