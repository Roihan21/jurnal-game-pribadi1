# setup_db_game.py
import sqlite3
import os
from konfigurasi import DB_PATH

def setup_database():
    """Membuat file database dan tabel 'games' jika belum ada."""
    print(f"Membuat database di: {DB_PATH}")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Perintah SQL untuk membuat tabel dengan semua kolom yang dibutuhkan
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            platform TEXT,
            genre TEXT,
            status TEXT,
            rating INTEGER,
            review_pribadi TEXT,
            url_cover_art TEXT
        );
        """)
        print("-> Tabel 'games' siap.")
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"-> Error SQLite saat setup: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("-> Koneksi DB setup ditutup.")

if __name__ == "__main__":
    print("--- Memulai Setup Database Jurnal Game ---")
    if setup_database():
        print(f"\nSetup database '{os.path.basename(DB_PATH)}' selesai.")
    else:
        print(f"\nSetup database GAGAL.")
