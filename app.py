# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import datetime
import os

nltk.download('vader_lexicon')

USERNAME = "admin"
PASSWORD = "123"

if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def analyze_sentiment(penilaian):
    if penilaian == "Baik":
        return "Positif"
    elif penilaian == "Sedang":
        return "Netral"
    elif penilaian == "Buruk":
        return "Negatif"
    else:
        return "Netral"

# ---------- Halaman Utama ----------
def home():
    st.title("📌 Analisis Sentimen Pelayanan SAMSAT")
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔐 Admin"):
            st.session_state.page = "login"
    st.write("Silakan pilih menu di bawah:")
    if st.button("📝 Isi Komentar"):
        st.session_state.page = "form"

# ---------- Form Komentar ----------
def form():
    st.title("🗣️ Form Komentar Publik")
    name = st.text_input("Nama")
    tanggal = st.date_input("Tanggal", value=datetime.date.today())
    sumber = st.selectbox("Mendapatkan informasi dari mana?", ["YouTube", "Instagram", "Google Maps", "WhatsApp", "Scan Ditempat"])
    penilaian = st.radio("Bagaimana pelayanannya?", ["Baik", "Sedang", "Buruk"])
    
    komentar = st.text_area("Berikan alasanmu:")
    if st.button("Kirim"):
        sentimen = analyze_sentiment(penilaian)
        data = {
            "Tanggal": tanggal,
            "Nama": name,
            "Sumber": sumber,
            "Penilaian": penilaian,
            "Komentar": komentar,
            "Sentimen": sentimen
        }
        df = pd.DataFrame([data])
        file_exists = os.path.isfile("data_komentar.csv")
        df.to_csv("data_komentar.csv", mode="a", header=not file_exists, index=False)
        st.session_state.page = "thanks"

# ---------- Terima Kasih ----------
def thanks():
    st.title("😊 Terima kasih atas partisipasi Anda!")
    if st.button("Kembali ke Beranda"):
        st.session_state.page = "home"

# ---------- Login Admin ----------
def login():
    st.title("🔒 Login Admin")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == USERNAME and pw == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
        else:
            st.error("Username atau password salah.")
    if st.button("Kembali"):
        st.session_state.page = "home"

# ---------- Dashboard ----------
def dashboard():
    st.title("📊 Dashboard Analisis Sentimen")

    if not os.path.exists("data_komentar.csv"):
        st.warning("Belum ada data komentar.")
        return

    df = pd.read_csv("data_komentar.csv")

    st.write("### Grafik Total Komentar per Platform")
    platform_counts = df["Sumber"].value_counts()
    st.bar_chart(platform_counts)

    st.write("### Grafik Hasil Sentimen")
    sentiment_counts = df["Sentimen"].value_counts()
    st.bar_chart(sentiment_counts)

    st.write("### Wordcloud Komentar")
    text = " ".join(df["Komentar"].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    st.write("### Insight dan Rekomendasi")
    st.info(f"""
    - Komentar positif menunjukkan pelayanan cukup memuaskan di beberapa platform.
    - Platform {platform_counts.idxmax()} adalah sumber komentar terbanyak.
    - Disarankan untuk menindaklanjuti komentar negatif dari platform {platform_counts.idxmin()}.
    - Tingkatkan pelayanan pada aspek yang sering disebut dalam komentar buruk.
    """)

    st.write("### Tabel Hasil Komentar")
    edited_df = df.copy()

    for i in range(len(edited_df)):
        col = st.columns([6, 1])
        with col[0]:
            st.write(edited_df.iloc[i].to_dict())
        with col[1]:
            if st.button("🗑️ Hapus", key=f"del_{i}"):
                df.drop(index=i, inplace=True)
                df.to_csv("data_komentar.csv", index=False)
                st.experimental_rerun()

    st.download_button("📥 Unduh CSV", df.to_csv(index=False).encode(), "komentar.csv", "text/csv")
    st.download_button("📥 Unduh TXT", df.to_string(index=False).encode(), "komentar.txt", "text/plain")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "home"

# ---------- Routing ----------
def main():
    page = st.session_state.page
    if page == "home":
        home()
    elif page == "form":
        form()
    elif page == "thanks":
        thanks()
    elif page == "login":
        login()
    elif page == "dashboard":
        if st.session_state.logged_in:
            dashboard()
        else:
            login()

if __name__ == "__main__":
    main()