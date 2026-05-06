import sqlite3
import os
from typing import List, Optional, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "location.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
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
                search_time TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Travel_Distance (
                travel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                distance_km REAL NOT NULL,
                destination TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Nearby_Places (
                place_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                place_name TEXT NOT NULL,
                category TEXT,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Notification_History (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                notification_time TEXT NOT NULL,
                esp32_pushed_time TEXT,
                app_name TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            )
            """)
            conn.commit()

    # --- User Operations ---
    def insert_user(self, username, email, hashed_password) -> Optional[int]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, hashed_password)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_users(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users")
            return [dict(row) for row in cursor.fetchall()]

    # --- Search Operations ---
    def insert_search(self, user_id, location_name, search_time):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Map_Search (user_id, location_name, search_time) VALUES (?, ?, ?)",
                (user_id, location_name, search_time)
            )
            conn.commit()
            return cursor.lastrowid

    def get_searches(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute("SELECT * FROM Map_Search WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT * FROM Map_Search")
            return [dict(row) for row in cursor.fetchall()]

    # --- Travel Operations ---
    def insert_travel(self, user_id, distance_km, destination):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Travel_Distance (user_id, distance_km, destination) VALUES (?, ?, ?)",
                (user_id, distance_km, destination)
            )
            conn.commit()
            return cursor.lastrowid

    def get_travel(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute("SELECT * FROM Travel_Distance WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT * FROM Travel_Distance")
            return [dict(row) for row in cursor.fetchall()]

    # --- Places Operations ---
    def insert_place(self, user_id, place_name, category):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Nearby_Places (user_id, place_name, category) VALUES (?, ?, ?)",
                (user_id, place_name, category)
            )
            conn.commit()
            return cursor.lastrowid

    def get_places(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute("SELECT * FROM Nearby_Places WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT * FROM Nearby_Places")
            return [dict(row) for row in cursor.fetchall()]

    # --- Notification Operations ---
    def insert_notification(self, user_id, time, app, content):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Notification_History (user_id, notification_time, app_name, content) VALUES (?, ?, ?, ?)",
                (user_id, time, app, content)
            )
            conn.commit()
            return cursor.lastrowid

    def get_notifications(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute("SELECT * FROM Notification_History WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT * FROM Notification_History")
            return [dict(row) for row in cursor.fetchall()]

# Singleton instance
db = DatabaseManager()
