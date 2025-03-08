# 🚴 Bike Sharing Dashboard

Proyek ini bertujuan untuk menganalisis data penyewaan sepeda menggunakan berbagai teknik eksplorasi data dan visualisasi interaktif dengan Streamlit.

## 📁 Struktur Proyek
```
submission
│── dashboard
│   ├── main_data.csv
│   ├── dashboard.py
│── data
│   ├── data_1.csv
│   ├── data_2.csv
│── notebook.ipynb
│── README.md
│── requirements.txt
│── url.txt
```

## ⚙️ Setup Environment di VSCode

Pastikan Python sudah terinstal di sistem Anda (disarankan versi 3.9).

1. Buka VSCode dan buka folder proyek.
2. Buka terminal di VSCode (`Ctrl + ~`).
3. Buat dan aktifkan virtual environment:

```sh
python -m venv env
source env/bin/activate  # Untuk macOS/Linux
env\Scripts\activate     # Untuk Windows
```

4. Instal dependensi:

```sh
pip install -r requirements.txt
```

## 🚀 Menjalankan Streamlit App
```sh
streamlit run dashboard/dashboard.py
```

## 📌 Catatan
- **dashboard.py**: Script utama untuk menjalankan Streamlit Dashboard.
- **notebook.ipynb**: Notebook untuk eksplorasi dan analisis data.
- **data/**: Folder yang berisi dataset terkait analisis.
- **requirements.txt**: Daftar dependensi yang dibutuhkan.
- **url.txt**: File untuk menyimpan informasi terkait proyek.

---
✨ **Proyek ini dikembangkan untuk analisis data penyewaan sepeda dengan Streamlit.** 🚴
