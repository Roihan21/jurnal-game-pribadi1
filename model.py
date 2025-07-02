# model.py
class Game:
    """
    Merepresentasikan satu entitas game dalam koleksi.
    Bertindak sebagai struktur data untuk membawa informasi game di dalam aplikasi.
    """
    def __init__(self, judul: str, platform: str, genre: str, status: str, 
                 rating: int = 0, review_pribadi: str = "", url_cover_art: str = "", 
                 id: int = None):
        self.id = id
        self.judul = judul
        self.platform = platform
        self.genre = genre
        self.status = status
        self.rating = rating
        self.review_pribadi = review_pribadi
        self.url_cover_art = url_cover_art

    def __repr__(self):
        """Representasi string untuk debugging."""
        return f"Game(ID: {self.id}, Judul: '{self.judul}')"
