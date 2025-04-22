"""送迎メッセージを通知する."""
import os
from datetime import datetime
import textwrap

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
user_pdf_url = "https://akashicsoftware.github.io/tclan_files/external_files/202504to202511.pdf"
# 担当者マップ
user_mapping = [
    (datetime(2025,3,31), datetime(2025,4,6), "若林"),
    (datetime(2025,4,7), datetime(2025,4,13), "荒木"),
    (datetime(2025,4,14), datetime(2025,4,20), "佐藤"),
    (datetime(2025,4,21), datetime(2025,4,27), "宮下"),
    (datetime(2025,4,28), datetime(2025,5,4), "澤"),
    (datetime(2025,5,5), datetime(2025,5,11), "坂野"),
    (datetime(2025,5,12), datetime(2025,5,18), "遠藤"),
    (datetime(2025,5,19), datetime(2025,5,25), "森"),
    (datetime(2025,5,26), datetime(2025,6,1), "伏黒"),
    (datetime(2025,6,2), datetime(2025,6,8), "小野"),
    (datetime(2025,6,9), datetime(2025,6,15), "浅野"),
    (datetime(2025,6,16), datetime(2025,6,22), "若林"),
    (datetime(2025,6,23), datetime(2025,6,29), "荒木"),
    (datetime(2025,6,30), datetime(2025,7,6), "小野"),
    (datetime(2025,7,7), datetime(2025,7,13), "宮下"),
    (datetime(2025,7,14), datetime(2025,7,20), "澤"),
    (datetime(2025,7,21), datetime(2025,7,27), "坂野"),
    (datetime(2025,7,28), datetime(2025,8,3), "遠藤"),
    (datetime(2025,8,4), datetime(2025,8,10), "森"),
    (datetime(2025,8,11), datetime(2025,8,17), "伏黒"),
    (datetime(2025,8,18), datetime(2025,8,24), "小野"),
    (datetime(2025,8,25), datetime(2025,8,31), "浅野"),
    (datetime(2025,9,1), datetime(2025,9,7), "若林"),
    (datetime(2025,9,8), datetime(2025,9,14), "荒木"),
    (datetime(2025,9,15), datetime(2025,9,21), "伏黒"),
    (datetime(2025,9,22), datetime(2025,9,28), "宮下"),
    (datetime(2025,9,29), datetime(2025,10,5), "澤"),
    (datetime(2025,10,6), datetime(2025,10,12), "坂野"),
    (datetime(2025,10,13), datetime(2025,10,19), "遠藤"),
    (datetime(2025,10,20), datetime(2025,10,26), "森"),
    (datetime(2025,10,27), datetime(2025,11,2), "伏黒"),
    (datetime(2025,11,3), datetime(2025,11,9), "小野"),
    (datetime(2025,11,10), datetime(2025,11,16), "浅野"),
    (datetime(2025,11,17), datetime(2025,11,23), "若林"),
    (datetime(2025,11,24), datetime(2025,11,30), "荒木"),
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


    def create_msg(self):
        """メッセージ作成."""
        # 実行日.
        if debug_config.get("is_debug_date", True):
            today = datetime(2025, 4, 28)
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
                                    "uri": user_pdf_url
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
