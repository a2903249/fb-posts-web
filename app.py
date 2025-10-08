# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 10:18:32 2025

@author: user
"""

from flask import Flask, render_template, redirect, url_for
import pandas as pd
import subprocess
import os
import sys

app = Flask(__name__)

CSV_PATH = "./posts.csv"

def read_posts():
    df = pd.read_csv(CSV_PATH)
    return df.to_dict(orient="records")

@app.route("/")
def index():
    posts = read_posts()
    return render_template("index.html", posts=posts)

@app.route("/update")
def update_posts():
    # 呼叫你的 update_posts.py 更新 CSV
    try:
        subprocess.run(
            [sys.executable, "fb-sdk.py"],  # 用目前 Python 執行
            check=True,
            cwd=os.path.dirname(os.path.abspath(__file__))  # 確保路徑正確
        )
        return redirect(url_for("index"))  # 成功後跳回首頁 /
    except subprocess.CalledProcessError as e:
        return f"更新失敗: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)