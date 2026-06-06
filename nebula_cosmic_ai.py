import requests
import sqlite3
import hashlib
from datetime import datetime

print("🌌" + "="*60)
print("     N E B U L A   C O S M I C   A I")
print("           เวอร์ชันสำหรับ Kodex")
print("="*60 + "\n")

GROQ_API_KEY = "gsk_ใส่_key_ของคุณ_ตรงนี้"   # ← เปลี่ยนตรงนี้สำคัญ

DB_PATH = "nebula_cosmic.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, created_at TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, user_id INTEGER, role TEXT, content TEXT, timestamp TEXT)''')
conn.commit()
conn.close()

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                  (username, hash_password(password), str(datetime.now())))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, role, content, str(datetime.now())))
    conn.commit()
    conn.close()

print("🌌 ยินดีต้อนรับสู่ Nebula Cosmic AI\n")

while True:
    print("\n1. เข้าสู่ระบบ")
    print("2. สมัครสมาชิกใหม่")
    print("3. ออก")
    choice = input("\nเลือกหมายเลข: ").strip()

    if choice == "1":
        username = input("ชื่อผู้ใช้: ").strip()
        password = input("รหัสผ่าน: ").strip()
        user_id = login_user(username, password)
        if user_id:
            print(f"\n✅ ยินดีต้อนรับ {username}!")
            break
        else:
            print("❌ ชื่อผู้ใช้หรือรหัสผ่านผิด")
    elif choice == "2":
        username = input("ตั้งชื่อผู้ใช้: ").strip()
        password = input("ตั้งรหัสผ่าน: ").strip()
        if register_user(username, password):
            print("✅ สมัครสำเร็จ! กรุณาเข้าสู่ระบบ")
        else:
            print("❌ ชื่อผู้ใช้นี้มีอยู่แล้ว")
    elif choice == "3":
        print("🌌 ลาก่อน...")
        break

print("\n🚀 Nebula Cosmic AI พร้อมใช้งานแล้ว พิมพ์ 'exit' เพื่อออก\n")

while True:
    user_input = input("คุณ: ").strip()
    if user_input.lower() in ['exit', 'quit', 'ออก', 'bye']:
        print("🌌 ลาก่อน...")
        break
    if not user_input:
        continue
    save_message(user_id, "user", user_input)
    print("🌠 Nebula กำลังคิด...")
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": user_input}], "temperature": 0.7},
            timeout=30
        )
        answer = response.json()["choices"][0]["message"]["content"]
        print(f"\n🌌 Nebula: {answer}\n")
        save_message(user_id, "assistant", answer)
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}\n")
