import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Konfigurasi tampilan Seaborn
sns.set_theme(style="whitegrid")

# Pastikan file `main_data.csv` dibaca dari folder yang sama
file_path = os.path.join(os.path.dirname(__file__), "main_data.csv")

# === Pengecekan File === #
if not os.path.exists(file_path):
    st.error(f"❌ File {file_path} tidak ditemukan! Pastikan file ada di direktori yang benar.")
    st.stop()

# === Fungsi untuk membaca data dengan caching (untuk performa) === #
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')  # Konversi ke datetime
        return df.dropna(subset=['dteday'])  # Hapus baris dengan tanggal kosong
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat membaca file CSV: {e}")
        st.stop()

# Load dataset
day_df = load_data(file_path)

# Mapping season ke nama yang lebih jelas
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_name'] = day_df['season'].map(season_map)

# Mapping weekday agar berurutan dengan benar
weekday_map = {0: 'Sen', 1: 'Sel', 2: 'Rab', 3: 'Kam', 4: 'Jum', 5: 'Sab', 6: 'Min'}
day_df['weekday_name'] = day_df['weekday'].map(weekday_map)

# === Header Aplikasi === #
st.title('🚴 Bike Sharing Dashboard')

# === Sidebar untuk Filter Musim === #
season_options = ['Semua Musim'] + list(day_df['season_name'].unique())
selected_season = st.sidebar.selectbox("🔍 Pilih Musim:", season_options)

# Filter Data berdasarkan musim
if selected_season == "Semua Musim":
    filtered_df = day_df.copy()
else:
    filtered_df = day_df[day_df['season_name'] == selected_season].copy()

# === Visualisasi Tren Peminjaman === #
st.subheader(f'📊 Tren Peminjaman Sepeda - {selected_season}')
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='dteday', y='cnt', data=filtered_df, ax=ax, marker='o', color='blue')
ax.set_xlabel('Tanggal', fontsize=12)
ax.set_ylabel('Total Peminjaman Sepeda', fontsize=12)
ax.set_title(f'Tren Peminjaman Sepeda selama {selected_season}', fontsize=14)
plt.xticks(rotation=45)
st.pyplot(fig)

# === Visualisasi Pengaruh Cuaca terhadap Peminjaman === #
st.subheader('🌦 Pengaruh Cuaca terhadap Peminjaman Sepeda')
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='weathersit', y='cnt', data=filtered_df, estimator=np.mean, ax=ax, palette='Set2')
ax.set_xlabel('Kondisi Cuaca (1=Cerah, 2=Berawan, 3=Hujan)', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman Sepeda', fontsize=12)
ax.set_title('Rata-rata Peminjaman Sepeda Berdasarkan Cuaca', fontsize=14)
st.pyplot(fig)

# === Visualisasi Peminjaman Berdasarkan Hari === #
st.subheader('🗓 Rata-rata Peminjaman Sepeda Berdasarkan Hari dalam Seminggu')

# Hitung rata-rata peminjaman per hari dan urutkan
weekday_avg = filtered_df.groupby('weekday_name')['cnt'].mean().reindex(['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'])

# Buat skala warna berdasarkan ranking nilai rata-rata
rank = weekday_avg.rank(method="first")  # Ranking dari yang terkecil ke terbesar
colors = sns.color_palette("Reds", len(weekday_avg))  # Palet warna dari terang ke gelap
rank_colors = [colors[int(r)-1] for r in rank]  # Ambil warna sesuai ranking

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=weekday_avg.index, y=weekday_avg.values, ax=ax, palette=rank_colors)
ax.set_xlabel('Hari dalam Seminggu', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman Sepeda', fontsize=12)
ax.set_title('Rata-rata Peminjaman Sepeda per Hari', fontsize=14)
st.pyplot(fig)

# === Informasi Tambahan === #
st.write('📌 Dashboard ini dibuat untuk menganalisis tren peminjaman sepeda berdasarkan faktor cuaca dan waktu.')
