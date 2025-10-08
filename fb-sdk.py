import facebook
import pandas as pd
from datetime import datetime, timedelta

# 1️⃣ 粉專 ID 與 Page Token
page_id = "1391633687742345"
page_token = "EAALZAJ9XpYpsBPukUP15POppYdgzqZAM83RAdIiDVT8J02vYVxyqLueI7RJdpFaGRpmamVlmaA0CUwUexKYBcQNxZAwphQGonNK2IZAMTh4E9yum2SeLtgQHfJ7YWVG9RXAyR9lQzHZAx7DADSh2tWlxUCwUiPl3lOcT2j4Xd9mg06XNjjO06Dv86tF69WCdY4GJVAvXLIAZDZD"
# output_file = r"C:/Users/user/Downloads/fb_posts_sdk.csv"
output_file = r"posts.csv"
# 2️⃣ 建立 GraphAPI 物件
graph = facebook.GraphAPI(access_token=page_token)

# 3️⃣ 抓粉專貼文（一次抓 100 篇以上，避免漏貼文）"
posts_data = graph.get_connections(
    id=page_id,
    connection_name='posts',
    fields='id,message,created_time,permalink_url,full_picture',
    limit=100
)
#print(posts_data)  #印出來看看長什麼樣子，會是JSON格式的資料
#print("Fanpage id = ", posts_data['id'])

# 4️⃣ 解析貼文並轉台灣時間
posts = []
for post in posts_data['data']:
    message = post.get('message', '')
    link = post.get('permalink_url', '')
    img = post.get('full_picture', '')

    created_time = post.get('created_time', '')
    if created_time:
        dt_utc = datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S%z")
        dt_tw = dt_utc + timedelta(hours=8)
    else:
        dt_tw = None

    posts.append({
        "created_time": dt_tw,
        "message": message,
        "full_picture": img,
        "permalink_url": link
    })

# 5️⃣ 排序並取最新 5 篇
latest_5 = sorted([p for p in posts if p["created_time"]], key=lambda x: x["created_time"], reverse=True)[:5]

# 6️⃣ 匯出 CSV，時間格式化
df = pd.DataFrame(latest_5)
df["created_time"] = df["created_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"✅ 最新 5 篇貼文已輸出到 {output_file}")
