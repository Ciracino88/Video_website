import sqlite3

class Post:
    def __init__(self, title, content, upload_date):
        self.title = title
        self.content = content
        self.upload_date = upload_date

    def upload_post(self):
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # 데이터 삽입
        c.execute('''
        INSERT INTO posts (title, content, upload_date)
        VALUES (?, ?, ?)
        ''', (self.title, self.content, self.upload_date))

        conn.commit()
        conn.close()