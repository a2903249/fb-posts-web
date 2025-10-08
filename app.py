# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 10:18:32 2025

@author: user
"""

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    # 讀取 CSV
    df = pd.read_csv('posts.csv')
    # 轉成 dict list 給模板使用
    posts = df.to_dict(orient='records')
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)