# manajer_game.py
from model import Game
import database as db
import pandas as pd # Tambahkan impor pandas

class ManajerGame:
    """
    Mengelola semua logika bisnis untuk koleksi game,
    termasuk menambah, mengambil, mengedit, dan menghapus data.
    """
    def __init__(self):
        """Konstruktor untuk ManajerGame."""
        pass

    def tambah_game(self, game: Game) -> bool:
        # ... (kode tambah_game tetap sama)
        sql = "INSERT INTO games (judul, platform, genre, status, rating, review_pribadi, url_cover_art) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params = (game.judul, game.platform, game.genre, game.status, game.rating, game.review_pribadi, game.url_cover_art)
        try:
            db.execute_query(sql, params)
            return True
        except Exception as e:
            print(f"ERROR [manajer_game.py] Gagal menambah game: {e}")
            return False

    def get_semua_game(self) -> list[Game]:
        # ... (kode get_semua_game tetap sama)
        sql = "SELECT * FROM games ORDER BY judul ASC"
        rows = db.fetch_query(sql)
        if not rows: return []
        daftar_game = []
        for row in rows:
            row_dict = dict(row)
            game_obj = Game(
                id=row_dict['id'], 
                judul=row_dict['judul'], 
                platform=row_dict.get('platform', 'Lainnya'), 
                genre=row_dict.get('genre', 'Lainnya'), 
                status=row_dict.get('status', 'Di Backlog'), 
                rating=row_dict.get('rating', 0), 
                review_pribadi=row_dict.get('review_pribadi', ''), 
                url_cover_art=row_dict.get('url_cover_art', '')
            )
            daftar_game.append(game_obj)
        return daftar_game

    def get_dataframe_koleksi(self) -> pd.DataFrame:
        """
        Metode baru untuk mengambil semua data game dan langsung mengembalikannya
        sebagai DataFrame Pandas untuk analisis.
        """
        sql = "SELECT * FROM games"
        # Gunakan fungsi yang ada di database.py jika Anda sudah membuatnya,
        # atau buat koneksi langsung di sini untuk mengambil data.
        conn = db.get_db_connection()
        if conn:
            try:
                df = pd.read_sql_query(sql, conn)
                return df
            finally:
                conn.close()
        return pd.DataFrame() # Kembalikan DataFrame kosong jika gagal

    def update_game(self, game: Game) -> bool:
        # ... (kode update_game tetap sama)
        sql = """UPDATE games SET judul = ?, platform = ?, genre = ?, status = ?, rating = ?, review_pribadi = ?, url_cover_art = ? WHERE id = ?"""
        params = (game.judul, game.platform, game.genre, game.status, game.rating, game.review_pribadi, game.url_cover_art, game.id)
        try:
            db.execute_query(sql, params)
            return True
        except Exception as e:
            print(f"ERROR [manajer_game.py] Gagal memperbarui game: {e}")
            return False
            
    def hapus_game(self, id_game: int) -> bool:
        # ... (kode hapus_game tetap sama)
        sql = "DELETE FROM games WHERE id = ?"
        params = (id_game,)
        try:
            db.execute_query(sql, params)
            return True
        except Exception as e:
            print(f"ERROR [manajer_game.py] Gagal menghapus game: {e}")
            return False
