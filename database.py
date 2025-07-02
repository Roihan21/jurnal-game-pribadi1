# database.py
import sqlite3
from konfigurasi import DB_PATH

def get_db_connection() -> sqlite3.Connection | None:
    """Membuka dan mengembalikan koneksi baru ke database SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Koneksi DB gagal: {e}")
        return None

def execute_query(query: str, params: tuple = None):
    """Menjalankan query yang mengubah data (INSERT, UPDATE, DELETE)."""
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Query gagal: {e} | Query: {query[:60]}")
        conn.rollback()
        return None
    finally:
        if conn: conn.close()

def fetch_query(query: str, params: tuple = None, fetch_all: bool = True):
    """Menjalankan query SELECT untuk mengambil data."""
    conn = get_db_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall() if fetch_all else cursor.fetchone()
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Fetch gagal: {e} | Query: {query[:60]}")
        return None
    finally:
        if conn: conn.close()
