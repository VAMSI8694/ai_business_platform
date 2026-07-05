from database import engine

try:
    conn = engine.connect()
    print("Connected to the database successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)