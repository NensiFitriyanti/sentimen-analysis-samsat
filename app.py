import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os
import time
nltk.download('vader_lexicon')

# Dummy login
USERNAME = "admin"
PASSWORD = "123"

# File komentar
CSV_FILE = "data_komentar.csv"

# Setup session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, parse_dates=["Waktu"])
    return pd.DataFrame(columns=["Platform", "Komentar", "Sentimen", "Waktu"])

def save_comment(platform, komentar, sentimen):
    df = load_data()
    new_row = pd.DataFrame({
        "Platform": [platform],
        "Komentar": [komentar],
        "Sentimen": [sentimen],
        "Waktu": [pd.Timestamp.now()]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def home_page():
    st.title("📊 Aplikasi Analisis Sentimen Pelayanan SAMSAT")
    st.write("Selamat datang! Silakan pilih menu:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Isi Komentar"):
            st.session_state.page = "form"
    with col2:
        if st.button("🔐 Masuk Dashboard (Admin)"):
            st.session_state.page = "login"

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
        st.success("✅ Terima kasih atas tanggapan Anda 🙏")
        time.sleep(3)
        st.session_state.page = "home"
        st.experimental_rerun()

def login_page():
    st.subheader("🔐 Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
            st.experimental_rerun()
        else:
            st.error("Username atau password salah!")

def dashboard_page():
    st.title("📈 Dashboard Analisis Sentimen")
    df = load_data()
    if df.empty:
        st.warning("Belum ada data komentar.")
        return

    # Statistik singkat
    col1, col2, col3 = st.columns(3)
    col1.metric("Positif", str(len(df[df["Sentimen"] == "Positif"])))
    col2.metric("Netral", str(len(df[df["Sentimen"] == "Netral"])))
    col3.metric("Negatif", str(len(df[df["Sentimen"] == "Negatif"])))

    st.subheader("📊 Grafik Sentimen")
    fig, ax = plt.subplots()
    df["Sentimen"].value_counts().plot(kind="bar", color=["green", "gray", "red"], ax=ax)
    ax.set_ylabel("Jumlah Komentar")
    ax.set_title("Distribusi Sentimen")
    st.pyplot(fig)

    st.subheader("☁️ Wordcloud Komentar")
    text = " ".join(df["Komentar"].dropna())
    wordcloud = WordCloud(width=800, height=300, background_color="white").generate(text)
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.imshow(wordcloud, interpolation="bilinear")
    ax2.axis("off")
    st.pyplot(fig2)

    st.subheader("📄 Tabel Komentar")
    st.dataframe(df)

    if st.button("🔙 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "home"
        st.experimental_rerun()

# Routing halaman
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "form":
    form_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    if st.session_state.logged_in:
        dashboard_page()
    else:
        st.session_state.page = "login"