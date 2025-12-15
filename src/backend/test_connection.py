from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()
url = os.getenv("DATABASE_URL")

print(f"📝 Connection String: {url[:50]}...")  # Zeigt Anfang

try:
    engine = create_engine(url)
    conn = engine.connect()
    print("✅ Connection erfolgreich!")
    conn.close()
except Exception as e:
    print(f"❌ Fehler: {e}")