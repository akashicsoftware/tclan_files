# tclan-files
指定の時間にLINE通知を行います。

# 動作環境
github actionsのworkflowで実行中。

# 初期設定
以下は、環境変数(.env / Repository secrets)に設定。
| キー                        | 概要                                       |
|----------------------------|--------------------------------------------|
| `LINE_API_TOKEN`            | LINEの APIキー                             |
| `LINE_USER_ID`              | デバッグ用個人のID                         |
| `LINE_GROUP_ID_MAIN_CHANNEL`| リマインド通知に使うメインチャンネルID    |
| `LINE_GROUP_ID_DRIVER_CHANNEL`| 送迎通知に使うチャンネルID              |

# グループIDの確認
## localtunnelで、check_line_group_id.pyを実行
- sudo apt update
- sudo apt install nodejs npm
- npm install -g localtunnel
- python check_line_group_id.py
- lt --port ポート番号
- 表示URLを、line deveroperコンソールでWebhook URLに設定(Webhookの利用=ON)
- BOTを該当グループに招待
