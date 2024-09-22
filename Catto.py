import os
import sqlite3
import json
import openai
import random
import asyncio
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("CATTO_API_KEY")

def choose_text():
    text = ""
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    posts = cur.execute('SELECT id, title, content FROM posts').fetchall()

    column_names = [description[0] for description in cur.description]
    data = refine_text(posts, column_names)

    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    conn.close()

def refine_text(rows, column_names):
    data = []
    for row in rows:
        record = dict(zip(column_names, row))
        for key, value in record.items():
            if isinstance(value, str):
                record[key] = value.replace("\r\n", " ").replace("\n", " ").replace("\\", " ")
        data.append(record)
    return data

# def generate_comment():
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "너는 공감 능력이 뛰어나고 친절한 Catto 라는 유저야."},
#             {"role": "user", "content": f"여기 네가 읽을 글이야 : {choose_text()}"}
#         ],
#         max_tokens=50
#     )
#
#     return response['choices'][0]['message']['content']