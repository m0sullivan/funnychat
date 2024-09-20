from flask import Flask, render_template, send_file, request
import sqlite3
import math

conn = sqlite3.connect('chats.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS chats(name text, chat text)''')
cursor.execute(f"INSERT INTO chats VALUES ('server','started the chat...')")
conn.commit()

app = Flask(__name__)

@app.route("/")
def root():
    name = ""
    try:
        name = request.args["name"]
        chat = request.args["chat"]
        cursor.execute(f"INSERT INTO chats VALUES ('{name}','{chat}')")
        conn.commit()

    except:
        pass

    cursor.execute(f"SELECT * FROM chats")
    fetched = cursor.fetchall()

    chats = []
    for i in range(len(fetched) - 1, max(0, len(fetched) - 100), -1):
        chats.append({"name": fetched[i][0], "chat": fetched[i][1]})

    return render_template("index.html", chats=chats, name=name)

@app.route("/bulma.min.css")
def bulma():
    return send_file("bulma\\css\\bulma.min.css")

@app.route("/index.css")
def indexDotCSS():
    return send_file("templates\\index.css")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)