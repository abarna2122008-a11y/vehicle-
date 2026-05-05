import sqlite3

# connect database
conn = sqlite3.connect("location.db")
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# ---------------------------
# WRITE FUNCTION
# ---------------------------
def insert_user(username, email, password):
    cursor.execute(
        "INSERT INTO Users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )
    conn.commit()

# ---------------------------
# READ FUNCTION
# ---------------------------
def get_users():
    cursor.execute("SELECT * FROM Users")
    return cursor.fetchall()

# ---------------------------
# UPDATE FUNCTION
# ---------------------------
def update_user(user_id, new_username):
    cursor.execute(
        "UPDATE Users SET username = ? WHERE user_id = ?",
        (new_username, user_id)
    )
    conn.commit()

# ---------------------------
# TESTING
# ---------------------------
try:
    insert_user("abhi", "abhi@gmail.com", "1234")
except:
    pass

print("Before update:", get_users())

update_user(1, "abhinav")

print("After update:", get_users())

conn.close()