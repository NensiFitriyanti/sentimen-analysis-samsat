# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

# Dummy login
USERNAME = "admin"
PASSWORD = "123"

if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    with st.form("Login Admin"):
        st.subheader("🔐 Login Admin")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        if login_btn:
            if username == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.success("Login berhasil!")
            else:
                st.error("Username atau password salah.")

def generate_wordcloud(text_data):
    text_combined = " ".join(text_data)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_combined)
    return wordcloud

def load_data():
    try:
        df = pd.read_csv("data_komentar.csv", parse_dates=["Waktu"])
        return df
    except Exception as e:
        st.warning(f"Belum ada data komentar atau terjadi kesalahan: {e}")
        return pd.DataFrame()

def dashboard():
    st.markdown("<h2 style='text-align:center; color:#003366;'>📋 Dashboard Sentimen Layanan Samsat</h2>", unsafe_allow_html=True)

    df = load_data()
    if df.empty:
        return

    # Total komentar per platform
    total_platform = df['Platform'].value_counts()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Instagram", f"{total_platform.get('Instagram', 0)} Komentar")
    col2.metric("YouTube", f"{total_platform.get('YouTube', 0)} Komentar")
    col3.metric("Google Maps", f"{total_platform.get('Google Maps', 0)} Komentar")
    col4.metric("WhatsApp", f"{total_platform.get('WhatsApp', 0)} Komentar")
    col5.metric("Scan di Tempat", f"{total_platform.get('Scan di Tempat', 0)} Komentar")

    st.divider()

    # Grafik jumlah komentar per platform
    komentar_per_platform = df['Platform'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.bar(komentar_per_platform.index, komentar_per_platform.values, color=['violet', 'salmon', 'skyblue', 'green', 'orange'])
    ax1.set_title("Jumlah Komentar per Platform")
    ax1.set_ylabel("Jumlah Komentar")
    st.pyplot(fig1)

    # Grafik distribusi sentimen
    distribusi = df['Sentimen'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(distribusi.values, labels=distribusi.index, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

    # Wordcloud
    st.subheader("📌 Wordcloud Komentar")
    wordcloud = generate_wordcloud(df['Komentar'].astype(str))
    st.image(wordcloud.to_array(), use_column_width=True)

    # Insight & Rekomendasi
    st.subheader("💡 Insight & Rekomendasi")
    st.markdown("""
    - 🎥 **YouTube** menunjukkan sentimen negatif tertinggi. Perlu evaluasi konten & interaksi pengguna.
    - 📸 **Instagram** didominasi komentar netral. Gunakan visual kampanye untuk dorong sentimen positif.
    - 🗺️ **Google Maps** lebih banyak komentar positif. Pertahankan pelayanan offline.
    - 💬 **WhatsApp** dapat dioptimalkan untuk respons cepat dan personal.
    - 📍 **Scan di Tempat** cukup efektif, pastikan sistem QR tidak error saat digunakan.
    """)

    # Tabel komentar
    st.subheader("📝 Data Komentar")
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "data_komentar.csv", "text/csv")

def main():
    colA, colB = st.columns([6, 1])
    with colB:
        if not st.session_state.logged_in:
            if st.button("🔐 Admin"):
                st.session_state.page = "login"
        else:
            st.success("Admin Login ✔")
            if st.button("🔓 Logout"):
                st.session_state.logged_in = False

    if st.session_state.page == "login":
        login()
    elif st.session_state.logged_in:
        dashboard()
    else:
        st.info("Selamat datang! Silakan login untuk melihat dashboard.")

if __name__ == "__main__":
    main()