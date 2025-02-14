from fastapi import FastAPI
import uvicorn
import sqlite3

app = FastAPI()


@app.get("/")
def root():
    sqlite_connection = sqlite3.connect('../../examplesDB.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    sqlite_connection.close()
    return result[0] if len(result) > 0 else {}


@app.get("/add")
def add(name: str, password: str):
    if len(name) == 0 or len(password) == 0:
        return {"success": False}

    sqlite_connection = sqlite3.connect('../../examplesDB.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
    sqlite_connection.commit()
    sqlite_connection.close()
    return {"success": True}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
