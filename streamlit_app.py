# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go # Impor library plotly
from model import Game
from manajer_game import ManajerGame
from konfigurasi import PLATFORM_GAME, STATUS_GAME, GENRE_GAME

st.set_page_config(page_title="Jurnal Game Pribadi", layout="wide")

@st.cache_resource
def get_game_manager():
    """Membuat instance ManajerGame dan menyimpannya di cache Streamlit."""
    return ManajerGame()

manajer = get_game_manager()

def halaman_tambah_game():
    # Fungsi ini tidak berubah
    st.header("Tambah Game Baru ke Koleksi")
    with st.form("form_game_baru", clear_on_submit=True):
        judul = st.text_input("Judul Game*")
        platform = st.selectbox("Platform*", PLATFORM_GAME, index=None, placeholder="Pilih platform...")
        genre = st.selectbox("Genre*", GENRE_GAME, index=None, placeholder="Pilih genre...")
        status = st.selectbox("Status*", STATUS_GAME, index=None, placeholder="Pilih status...")
        rating = st.slider("Rating Pribadi (Bintang)", 0, 5, 0)
        url_cover = st.text_input("URL Cover Art (Opsional)", placeholder="Contoh: https://url.com/gambar.jpg")
        review = st.text_area("Review Singkat (Opsional)")
        submitted = st.form_submit_button("Simpan Game")
        if submitted:
            if not all([judul, platform, genre, status]):
                st.warning("Judul, Platform, Genre, dan Status wajib diisi!")
            else:
                game_baru = Game(judul, platform, genre, status, rating, review, url_cover)
                if manajer.tambah_game(game_baru):
                    st.success("Game berhasil disimpan!")
                else:
                    st.error("Gagal menyimpan game.")

def halaman_koleksi_saya():
    # Fungsi ini tidak berubah
    st.header("Koleksi Game Saya")
    daftar_game = manajer.get_semua_game()
    if not daftar_game:
        st.info("Koleksi game Anda masih kosong.")
        return
    status_filter = st.multiselect("Filter Status:", options=STATUS_GAME)
    platform_filter = st.multiselect("Filter Platform:", options=PLATFORM_GAME)
    genre_filter = st.multiselect("Filter Genre:", options=GENRE_GAME)
    filtered_games = daftar_game
    if status_filter: filtered_games = [g for g in filtered_games if g.status in status_filter]
    if platform_filter: filtered_games = [g for g in filtered_games if g.platform in platform_filter]
    if genre_filter: filtered_games = [g for g in filtered_games if g.genre in genre_filter]
    if not filtered_games:
        st.warning("Tidak ada game yang cocok dengan filter Anda.")
        return
    cols = st.columns(4) 
    for i, game in enumerate(filtered_games):
        with cols[i % 4]:
            with st.container(border=True):
                image_url = game.url_cover_art or "https://placehold.co/300x400/222/fff?text=No+Image"
                st.image(image_url, use_container_width=True)
                st.subheader(game.judul)
                st.write(f"**Platform:** {game.platform}")
                st.write(f"**Genre:** {game.genre}")
                st.write(f"**Status:** {game.status}")
                st.write(f"**Rating:** {'⭐' * game.rating or 'Belum ada rating'}")
                if game.review_pribadi:
                    with st.expander("Lihat Review"):
                        st.info(game.review_pribadi)
                with st.expander("Edit Game Ini"):
                    with st.form(key=f"edit_form_{game.id}"):
                        judul_baru = st.text_input("Judul Game*", value=game.judul)
                        platform_baru = st.selectbox("Platform*", PLATFORM_GAME, index=PLATFORM_GAME.index(game.platform) if game.platform in PLATFORM_GAME else 0)
                        genre_baru = st.selectbox("Genre*", GENRE_GAME, index=GENRE_GAME.index(game.genre) if game.genre in GENRE_GAME else 0)
                        status_baru = st.selectbox("Status*", STATUS_GAME, index=STATUS_GAME.index(game.status) if game.status in STATUS_GAME else 0)
                        rating_baru = st.slider("Rating (Bintang)", 0, 5, value=game.rating)
                        url_cover_baru = st.text_input("URL Cover Art", value=game.url_cover_art)
                        review_baru = st.text_area("Review Singkat", value=game.review_pribadi)
                        edit_submitted = st.form_submit_button("Simpan Perubahan")
                        if edit_submitted:
                            game_update = Game(judul_baru, platform_baru, genre_baru, status_baru, rating_baru, review_baru, url_cover_baru, id=game.id)
                            if manajer.update_game(game_update):
                                st.success(f"'{game.judul}' berhasil diperbarui!")
                                st.rerun()
                            else:
                                st.error("Gagal memperbarui game.")
                if st.button("Hapus", key=f"hapus_{game.id}", type="primary", use_container_width=True):
                    if manajer.hapus_game(game.id):
                        st.success(f"'{game.judul}' berhasil dihapus!")
                        st.rerun() 
                    else:
                        st.error("Gagal menghapus game.")

def halaman_analisis():
    """
    Fungsi untuk menampilkan halaman analisis dengan Radar Chart yang sudah diberi warna.
    """
    st.header("Analisis Koleksi Game")
    
    df = manajer.get_dataframe_koleksi()

    if df.empty or len(df) < 3:
        st.info("Belum ada cukup data untuk dianalisis. Silakan tambahkan minimal 3 game.")
        return

    # --- 1. Analisis Jumlah Game per Genre ---
    st.subheader("Distribusi Game Berdasarkan Genre")
    genre_counts = df['genre'].value_counts()
    
    fig_genre = go.Figure()
    fig_genre.add_trace(go.Scatterpolar(
          r=genre_counts.values,
          theta=genre_counts.index,
          fill='toself',
          name='Jumlah Game',
          line_color='darkviolet'
    ))
    # --- PERUBAHAN TEMA GRAFIK ---
    fig_genre.update_layout(
      paper_bgcolor='rgba(0,0,0,0)', # Latar belakang transparan
      polar=dict(
          radialaxis=dict(visible=True, range=[0, max(genre_counts.values)], gridcolor="grey", tickfont=dict(color="white")),
          angularaxis=dict(tickfont=dict(color="white"), linecolor="grey")
      ),
      showlegend=False,
      title=dict(text="Jumlah Game per Genre", font=dict(color="white"))
    )
    st.plotly_chart(fig_genre, use_container_width=True)

    st.divider()

    # --- 2. Analisis Jumlah Game per Platform ---
    st.subheader("Distribusi Game Berdasarkan Platform")
    platform_counts = df['platform'].value_counts()
    
    fig_platform = go.Figure()
    fig_platform.add_trace(go.Scatterpolar(
          r=platform_counts.values,
          theta=platform_counts.index,
          fill='toself',
          name='Jumlah Game',
          line_color='dodgerblue'
    ))
    # --- PERUBAHAN TEMA GRAFIK ---
    fig_platform.update_layout(
      paper_bgcolor='rgba(0,0,0,0)', # Latar belakang transparan
      polar=dict(
          radialaxis=dict(visible=True, range=[0, max(platform_counts.values)], gridcolor="grey", tickfont=dict(color="white")),
          angularaxis=dict(tickfont=dict(color="white"), linecolor="grey")
      ),
      showlegend=False,
      title=dict(text="Jumlah Game per Platform", font=dict(color="white"))
    )
    st.plotly_chart(fig_platform, use_container_width=True)

    st.divider()

    # --- 3. Analisis Rata-rata Rating per Genre ---
    st.subheader("Analisis Rata-rata Rating per Genre")
    rated_games_df = df[df['rating'] > 0]
    
    if rated_games_df.empty or len(rated_games_df) < 3:
        st.warning("Belum ada cukup game yang diberi rating (minimal 3) untuk dianalisis.")
    else:
        avg_rating_by_genre = rated_games_df.groupby('genre')['rating'].mean()
        
        fig_rating_genre = go.Figure()
        fig_rating_genre.add_trace(go.Scatterpolar(
              r=avg_rating_by_genre.values,
              theta=avg_rating_by_genre.index,
              fill='toself',
              name='Rata-rata Rating',
              line_color='gold'
        ))
        # --- PERUBAHAN TEMA GRAFIK ---
        fig_rating_genre.update_layout(
          paper_bgcolor='rgba(0,0,0,0)', # Latar belakang transparan
          polar=dict(
              radialaxis=dict(visible=True, range=[0, 5], gridcolor="grey", tickfont=dict(color="white")),
              angularaxis=dict(tickfont=dict(color="white"), linecolor="grey")
          ),
          showlegend=False,
          title=dict(text="Rata-rata Rating per Genre", font=dict(color="white"))
        )
        st.plotly_chart(fig_rating_genre, use_container_width=True)

def main():
    """Fungsi utama untuk menjalankan aplikasi dan mengatur navigasi."""
    st.sidebar.title("🎮 Jurnal Game Pribadi")
    menu_pilihan = st.sidebar.radio("Pilih Halaman:", ["Koleksi Saya", "Tambah Game", "Analisis"])
    st.sidebar.markdown("---")
    st.sidebar.info("Tugas Besar PBO")

    if menu_pilihan == "Koleksi Saya":
        halaman_koleksi_saya()
    elif menu_pilihan == "Tambah Game":
        halaman_tambah_game()
    elif menu_pilihan == "Analisis":
        halaman_analisis()

if __name__ == "__main__":
    main()
