"""グループID確認用."""
from flask import Flask, request

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    """受信したJSONデータの出力."""
    data = request.get_json()
    print(data)
    return "OK", 200

if __name__ == "__main__":
    app.run(port=8000)
