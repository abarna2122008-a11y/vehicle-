import sqlite3

# ---------------- CONNECT ----------------
conn = sqlite3.connect("location.db")
cursor = conn.cursor()

# ---------------- CREATE TABLES ----------------
try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Map_Search (
        search_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        location_name TEXT NOT NULL,
        search_time TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Travel_Distance (
        travel_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        distance_km REAL NOT NULL,
        destination TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Nearby_Places (
        place_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        place_name TEXT NOT NULL,
        category TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Notification_History (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        notification_time TEXT NOT NULL,
        esp32_pushed_time TEXT,
        app_name TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)

    conn.commit()
    print("Tables created successfully")

except Exception as e:
    print("Error creating tables:", e)

# ---------------- USERS ----------------
def insert_user(username, email, password):
    try:
        cursor.execute(
            "INSERT INTO Users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
        print("User inserted")
    except sqlite3.IntegrityError:
        print("User already exists (duplicate email)")
    except Exception as e:
        print("Error inserting user:", e)

def get_users():
    try:
        cursor.execute("SELECT * FROM Users")
        return cursor.fetchall()
    except:
        return []

def update_user(user_id, new_username):
    try:
        cursor.execute(
            "UPDATE Users SET username = ? WHERE user_id = ?",
            (new_username, user_id)
        )
        conn.commit()
    except Exception as e:
        print("Update error:", e)

# ---------------- MAP SEARCH ----------------
def insert_search(user_id, location_name, search_time):
    try:
        cursor.execute(
            "INSERT INTO Map_Search VALUES (NULL, ?, ?, ?)",
            (user_id, location_name, search_time)
        )
        conn.commit()
    except Exception as e:
        print("Search insert error:", e)

def get_searches():
    try:
        cursor.execute("SELECT * FROM Map_Search")
        return cursor.fetchall()
    except:
        return []

# ---------------- TRAVEL ----------------
def insert_travel(user_id, distance_km, destination):
    try:
        cursor.execute(
            "INSERT INTO Travel_Distance VALUES (NULL, ?, ?, ?)",
            (user_id, distance_km, destination)
        )
        conn.commit()
    except Exception as e:
        print("Travel insert error:", e)

def get_travel():
    try:
        cursor.execute("SELECT * FROM Travel_Distance")
        return cursor.fetchall()
    except:
        return []

# ---------------- PLACES ----------------
def insert_place(user_id, place_name, category):
    try:
        cursor.execute(
            "INSERT INTO Nearby_Places VALUES (NULL, ?, ?, ?)",
            (user_id, place_name, category)
        )
        conn.commit()
    except Exception as e:
        print("Place insert error:", e)

def get_places():
    try:
        cursor.execute("SELECT * FROM Nearby_Places")
        return cursor.fetchall()
    except:
        return []

# ---------------- NOTIFICATIONS ----------------
def insert_notification(user_id, time, app, content):
    try:
        cursor.execute(
            "INSERT INTO Notification_History VALUES (NULL, ?, ?, NULL, ?, ?)",
            (user_id, time, app, content)
        )
        conn.commit()
    except Exception as e:
        print("Notification insert error:", e)

def get_notifications():
    try:
        cursor.execute("SELECT * FROM Notification_History")
        return cursor.fetchall()
    except:
        return []

# ---------------- TEST ----------------
insert_user("abhi", "abhi@gmail.com", "1234")

print("Users:", get_users())

insert_search(1, "Chennai", "10:00 AM")
print("Search:", get_searches())

insert_travel(1, 12.5, "Airport")
print("Travel:", get_travel())

insert_place(1, "Hotel Saravana", "Restaurant")
print("Places:", get_places())

insert_notification(1, "10:05 AM", "Maps", "Route calculated")
print("Notifications:", get_notifications())

conn.close()