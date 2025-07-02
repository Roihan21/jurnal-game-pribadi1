# konfigurasi.py
import os

# Menentukan lokasi absolut dari file database untuk menghindari kebingungan path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'jurnal_game.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

# Daftar pilihan yang akan digunakan secara konsisten di seluruh aplikasi
PLATFORM_GAME = [
    "PC", 
    "PlayStation 5", 
    "PlayStation 4", 
    "Xbox Series X/S", 
    "Xbox One", 
    "Nintendo Switch", 
    "Mobile", 
    "Lainnya"
]

STATUS_GAME = [
    "Wishlist", 
    "Sedang Dimainkan", 
    "Selesai", 
    "Ditinggalkan", 
    "Terus Dimainkan"
]

GENRE_GAME = [
    "Action", 
    "Adventure",
    "RPG", 
    "JRPG",
    "Strategy", 
    "Sports", 
    "Simulation", 
    "Puzzle", 
    "Horror", 
    "Lainnya"
]
