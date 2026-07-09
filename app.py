
from flask import Flask, request
import pandas as pd
from datetime import datetime
import ssl
import time


# SSLエラー回避（ローカル用）
ssl._create_default_https_context = ssl._create_unverified_context


app = Flask(__name__)




# GoogleスプレッドシートCSV
URL = "https://docs.google.com/spreadsheets/d/1L5HVMn2S95UYrffuskYTihLmTa9YuXerVrOvb6FcC60/gviz/tq?tqx=out:csv"



#*****スプレッドシートからデータ取得*******
def get_data():
   #URLに現在時刻を付けてキャッシュ対策
   df = pd.read_csv(URL + "&t=" + str(time.time()))
   #スプシのカラム名の前後スペースを削除(error対策)
   df.columns = df.columns.str.strip()
   #id列を文字列に変換＋空白削除
   df["id"] = df["id"].astype(str).str.strip()
   return df


#******動作確認page*********
@app.route("/")
def home():
   return "OK - cert system running"


#******資格証表示page*********
@app.route("/cert")
def cert():
   #URLパラメータ(”?”以降)からtokenを取得
   #URL例: https://rope-access-association.com/cert?token=a57c721a3b93487e
   token = str(request.args.get("token", "")).strip()
   #スプレッドシートのデータ取得
   df = get_data()
   #tokenが一致する行を抽出
   row = df[df["token"] == token]
  
   #****該当データがない場合に表示するHTMLのerror画面)*****
   if row.empty:
       return f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{
   font-family: sans-serif;
   background: linear-gradient(135deg, #f5f5f5, #e0e0e0);
   display: flex;
   justify-content: center;
   align-items: center;
   height: 100vh;
   margin: 0;
}}


.card {{
   background: white;
   padding: 40px;
   border-radius: 20px;
   box-shadow: 0 8px 25px rgba(0,0,0,0.15);
   text-align: center;
   max-width: 400px;
}}


.title {{
   font-size: 24px;
   font-weight: bold;
   margin-bottom: 20px;
   color: #333;
}}


.message {{
   font-size: 16px;
   color: #555;
   margin-bottom: 25px;
   line-height: 1.6;
}}


.contact {{
   font-size: 14px;
   color: #888;
}}


.highlight {{
   color: #007BFF;
   font-weight: bold;
}}


.icon {{
   font-size: 50px;
   margin-bottom: 15px;
}}
</style>
</head>


<body>


<div class="card">
   <div class="icon">⚠️</div>


   <div class="title">
       表示エラー
   </div>


   <div class="message">
       申し訳ありません。<br>
       何かしらの不具合が発生しており、<br>
       正常に表示できません。
   </div>


   <div class="contact">
       <span class="highlight">keystone@rope-access.co.jp</span><br>
       または<br>
       <span class="highlight">075-959-9095</span><br>
       までご連絡ください。
   </div>
</div>


</body>
</html>
"""


   #****rowからdata取り出し******
   name = row.iloc[0]["name"]

   cert_id = row.iloc[0]["id"]
   image_url = row.iloc[0]["photo"]


   #*****固定表示text*********
   certification1 = "資格名称:SORAT レベル１"
   organization = "認定機関:(一社)ロープアクセス技術協会/(株)きぃすとん"

   status = "有効な資格証です"
   color = "green"



   #****logo画像*******
   logo1 = "https://res.cloudinary.com/duigqzi2c/image/upload/v1777346294/logo2_kyoukai_ac2rw4.jpg"
   logo2 = "https://res.cloudinary.com/duigqzi2c/image/upload/v1777269580/IMG_4632_ouetje.jpg"


   return f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">


<style>
body {{
   font-family: sans-serif;
   text-align: center;
   padding: 20px;
   background: #f5f5f5;
}}


.card {{
   background: white;
   padding: 25px;
   border-radius: 20px;
   box-shadow: 0 4px 15px rgba(0,0,0,0.1);
   max-width: 400px;
   margin: 0 auto;
}}


.name {{
   font-size: 28px;
   font-weight: bold;
   margin-bottom: 15px;
}}


.id {{
   font-size: 18px;
   margin-bottom: 8px;
}}


.status {{
   font-size: 32px;
   font-weight: bold;
   color: {color};
   white-space: nowrap;
   margin-bottom: 20px;
}}


.meta {{
   text-align: left;
   margin-top: 10px;
   font-size: 10px;
}}


.row {{
   display: flex;
   gap: 5px;
   margin-bottom: 6px;
}}


.label {{
   color: #000;
}}


.value {{
   color: #000;
}}


.logos {{
   display: flex;
   justify-content: center;
   align-items: center;
   gap: 10px;
   margin-bottom: 15px;
   transform: translateX(-10px);
}}


.logos img {{
   width: 130px;
   height: auto;
   object-fit: contain;
   border-radius: 0;
}}






@media (max-width: 600px) {{
   .card {{
       width: 90%;
       padding: 20px;
   }}


   .name {{
       font-size: 24px;
   }}


   .status {{
       font-size: 26px;
   }}
}}
</style>


</head>


<body>


<div class="card">


   <img src="{image_url}" style="width:120px;height:120px;border-radius:50%;object-fit:cover;margin-bottom:15px;">


   <div class="name">{name}</div>


   <div class="id">認定番号: {cert_id}</div>



   <div class="status">{status}</div>


   <div class="logos">
       <img src="{logo1}">
       <img src="{logo2}">
   </div>


   <div class="meta">


       <div class="row">
           <span class="value">{certification1}</span>
       </div>



       <div class="row">
           <span class="value">{organization}</span>
       </div>


   </div>


</div>


</body>
</html>
"""


#(保留)Render安定用に追加したけど使ってない
import os
#*******アプリ起動***********
if __name__ == "__main__":
   #0.0.0.0 → Renderの serverの中で動いているアプリを、みんなのスマホやPCから見れる
   #default(10000番)を使ってる
   #debug=True → error時に詳細表示
   app.run(host="0.0.0.0", port=10000, debug=True)





