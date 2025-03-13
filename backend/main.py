from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=db")
cur = conn.cursor()

class User(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(user: User):
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
        conn.commit()
        return {"message": "User registered"}
    except:
        raise HTTPException(status_code=400, detail="User already exists")

@app.post("/login")
def login(user: User):
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user.username, user.password))
    if cur.fetchone():
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")