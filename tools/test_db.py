# tools/test_db.py
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

url = os.environ.get("DATABASE_URL")
if not url:
    raise SystemExit("DATABASE_URL not set in .env")

print("Testing DB URL:", url)

# create engine and try a simple query
engine = create_engine(url, connect_args={"connect_timeout": 5})

try:
    with engine.connect() as conn:
        r = conn.execute(text("SELECT 1"))
        print("Database connection OK, SELECT 1 ->", r.scalar())
except Exception as e:
    print("Connection failed:", repr(e))
