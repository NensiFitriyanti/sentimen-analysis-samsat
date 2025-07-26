import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import datetime

nltk.download("vader_lexicon")

# Konstanta login
USERNAME = "admin"
PASSWORD = "123"

# Cek halaman
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Fungsi simpan komentar
def save_comment(platform, komentar, sentimen):
    df = pd.DataFrame([{
        "Platform": platform,
        "Komentar": komentar,
        "Sentimen": sentimen,
        "Waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    try:
        df_existing = pd.read_csv("data_komentar.csv")
        df_combined = pd.concat([df_existing, df], ignore_index=True)
    except FileNotFoundError:
        df_combined = df
    df_combined.to_csv("data_komentar.csv", index=False)

# Halaman form publik
def form_page():
    st.header("📝 Form Komentar Publik")
    nama = st.text_input("Nama lengkap")
    platform = st.selectbox("Dari mana Anda mendapatkan link pelayanan?", 
                            ["Instagram", "YouTube", "Google Maps", "WhatsApp", "Scan di Tempat"])
    pelayanan = st.radio("Bagaimana pendapat Anda tentang pelayanan kami?", 
                         ["Baik", "Sedang", "Buruk"])
    komentar = st.text_area("Berikan komentar/alasan Anda")

    if st.button("Kirim"):
        if pelayanan == "Baik":
            sentimen = "Positif"
        elif pelayanan == "Sedang":
            sentimen = "Netral"
        else:
            sentimen = "Negatif"
        save_comment(platform, komentar, sentimen)
        st.session_state.page = "thanks"
        st.experimental_rerun()

# Halaman ucapan terima kasih
def thanks_page():
    st.success("✅ Terima kasih atas tanggapan Anda 🙏")
    st.write("Anda akan diarahkan kembali ke halaman utama...")
    st.markdown("""
        <meta http-equiv="refresh" content="3;url=." />
    """, unsafe_allow_html=True)

# Halaman dashboard admin
def dashboard_page():
    st.title("📊 Dashboard Admin - Analisis Sentimen")

    try:
        df = pd.read_csv("data_komentar.csv")
    except FileNotFoundError:
        st.warning("Belum ada data komentar.")
        return

    # Tampilkan total komentar per platform
    st.subheader("📌 Total Komentar per Platform")
    st.dataframe(df["Platform"].value_counts().reset_index().rename(columns={"index": "Platform", "Platform": "Jumlah"}))

    # Grafik sentimen
    st.subheader("📈 Distribusi Sentimen")
    fig, ax = plt.subplots()
    df["Sentimen"].value_counts().plot(kind="bar", color=["green", "gray", "red"], ax=ax)
    ax.set_ylabel("Jumlah")
    ax.set_title("Sentimen Komentar")
    st.pyplot(fig)

    # Wordcloud
    st.subheader("☁️ WordCloud Komentar")
    all_text = " ".join(df["Komentar"].dropna().astype(str))
    if all_text:
        wordcloud = WordCloud(background_color="white", width=800, height=300).generate(all_text)
        fig_wc, ax_wc = plt.subplots(figsize=(10, 3))
        ax_wc.imshow(wordcloud, interpolation="bilinear")
        ax_wc.axis("off")
        st.pyplot(fig_wc)
    else:
        st.write("Tidak ada komentar untuk ditampilkan.")

# Halaman login admin
def login_page():
    st.subheader("🔐 Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
            st.success("Login berhasil!")
            st.experimental_rerun()
        else:
            st.error("Username atau password salah!")

# Halaman utama
def home_page():
    st.markdown("<h1 style='font-size: 32px;'>Sistem Analisis Sentimen Pelayanan SAMSAT</h1>", unsafe_allow_html=True)
    st.markdown("Selamat datang! Silakan pilih aksi di bawah ini.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Isi Komentar"):
            st.session_state.page = "form"
            st.experimental_rerun()
    with col2:
        if st.button("🔐 Masuk Dashboard (Admin)"):
            st.session_state.page = "login"
            st.experimental_rerun()

# Routing
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "form":
    form_page()
elif st.session_state.page == "thanks":
    thanks_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    if st.session_state.logged_in:
        dashboard_page()
    else:
        st.warning("Silakan login terlebih dahulu.")
        st.session_state.page = "login"
        st.experimental_rerun()
