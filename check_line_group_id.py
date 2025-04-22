import os

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    print(data)
    return "OK", 200


if __name__ == "__main__":
    app.run(port=8000)
