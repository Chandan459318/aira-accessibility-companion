import sqlite3

conn = sqlite3.connect("data/messages.db")
c = conn.cursor()

# Check if 'status' column already exists
c.execute("PRAGMA table_info(messages)")
columns = [col[1] for col in c.fetchall()]
if 'status' not in columns:
    c.execute("ALTER TABLE messages ADD COLUMN status TEXT DEFAULT 'sent'")
    print("✅ 'status' column added successfully.")
else:
    print("ℹ️ 'status' column already exists.")

conn.commit()
conn.close()
