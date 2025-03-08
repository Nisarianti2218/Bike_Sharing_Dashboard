import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Konfigurasi tampilan Seaborn
sns.set_theme(style="whitegrid")

# Pastikan `main_data.csv` dibaca dari folder yang sama dengan `dashboard.py`
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
        df['dteday'] = pd.to_datetime(df['dteday'])  # Konversi ke tipe datetime
        return df
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat membaca file CSV: {e}")
        st.stop()

# Load dataset
day_df = load_data(file_path)

# Mapping season ke nama yang lebih jelas
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_name'] = day_df['season'].map(season_map)

# === Header Aplikasi === #
st.title('🚴 Bike Sharing Dashboard')

# === Sidebar untuk Filter Musim === #
selected_season = st.sidebar.selectbox("🔍 Pilih Musim:", day_df['season_name'].unique())

# Filter Data berdasarkan musim
filtered_df = day_df[day_df['season_name'] == selected_season].copy()

# === Visualisasi Tren Peminjaman === #
st.subheader(f'📊 Tren Peminjaman Sepeda - {selected_season}')
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='dteday', y='cnt', data=filtered_df, ax=ax, marker='o', color='blue')
ax.set_xlabel('Tanggal', fontsize=12)
ax.set_ylabel('Total Peminjaman Sepeda', fontsize=12)
ax.set_title(f'Tren Peminjaman Sepeda selama Musim {selected_season}', fontsize=14)
plt.xticks(rotation=45)
st.pyplot(fig)

# === Visualisasi Pengaruh Cuaca terhadap Peminjaman === #
st.subheader('🌦 Pengaruh Cuaca terhadap Peminjaman Sepeda')
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x='weathersit', y='cnt', data=filtered_df, ax=ax, palette='Set2')
ax.set_xlabel('Kondisi Cuaca (1=Cerah, 2=Berawan, 3=Hujan)', fontsize=12)
ax.set_ylabel('Total Peminjaman Sepeda', fontsize=12)
ax.set_title('Distribusi Peminjaman Sepeda Berdasarkan Cuaca', fontsize=14)
st.pyplot(fig)

# === Visualisasi Peminjaman Berdasarkan Hari === #
st.subheader('📅 Rata-rata Peminjaman Sepeda Berdasarkan Hari dalam Seminggu')
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='weekday', y='cnt', data=filtered_df, estimator=np.mean, ax=ax, palette='pastel')
ax.set_xlabel('Hari dalam Seminggu (0=Senin, 6=Minggu)', fontsize=12)
ax.set_ylabel('Rata-rata Peminjaman Sepeda', fontsize=12)
ax.set_title('Rata-rata Peminjaman Sepeda per Hari', fontsize=14)
st.pyplot(fig)

# === Informasi Tambahan === #
st.write('📌 Dashboard ini dibuat untuk menganalisis tren peminjaman sepeda berdasarkan faktor cuaca dan waktu.')
