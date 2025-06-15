# Aplikasi Prediksi Kesehatan Mental

Aplikasi web untuk memprediksi kondisi kesehatan mental menggunakan algoritma K-Means clustering dengan 4 klaster.

## Fitur

- **Kuesioner Kesehatan Mental**: 11 pertanyaan tentang pola tidur, aktivitas, dan kondisi mental
- **Prediksi dengan 4 Klaster**:
  - Klaster 0: Kesehatan Mental Optimal
  - Klaster 1: Kesehatan Mental Baik
  - Klaster 2: Perlu Perhatian
  - Klaster 3: Risiko Kesehatan Mental
- **Visualisasi Interaktif**:
  - Radar chart untuk profil kesehatan mental
  - Bar chart untuk hasil klasifikasi
- **Rekomendasi Personal**: Saran spesifik berdasarkan klaster
- **Interface Responsif**: Desain yang mobile-friendly

## Instalasi

1. **Clone repository**:
   \`\`\`bash
   git clone <repository-url>
   cd mental-health-prediction
   \`\`\`

2. **Install dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Siapkan data dan model**:
   - Pastikan file `dataCleaning.xlsx` ada di direktori utama
   - Jalankan script training:
     \`\`\`bash
     python train_model.py
     \`\`\`
   - Script ini akan membuat file `kmeans_model.pkl` dan `scaler.pkl`

4. **Jalankan aplikasi**:
   \`\`\`bash
   python app.py
   \`\`\`

5. **Akses aplikasi**:
   - Buka browser dan kunjungi `http://localhost:5000`

## Struktur File

\`\`\`
├── app.py                 # Aplikasi Flask utama
├── train_model.py         # Script untuk training model
├── requirements.txt       # Dependencies Python
├── templates/
│   ├── index.html        # Halaman utama dengan form
│   └── result.html       # Halaman hasil prediksi
├── static/
│   └── script.js         # JavaScript untuk interaksi dan visualisasi
├── kmeans_model.pkl      # Model K-Means yang sudah dilatih
├── scaler.pkl           # Scaler untuk normalisasi data
└── dataCleaning.xlsx    # Data training (harus disediakan)
\`\`\`

## API Endpoints

- `GET /`: Halaman utama dengan form kuesioner
- `POST /predict`: Endpoint untuk prediksi (menerima JSON atau form data)
- `GET /result`: Halaman hasil prediksi (untuk form submission)

## Format Data Input

Data input harus berisi 11 fitur berikut:
- `Waktu_Tidur`: Jam tidur per malam (float)
- `Kualitas_Tidur`: Skala 1-5 (int)
- `Kesulitan_Tidur`: Skala 1-5 (int)
- `Kebugaran_Bangun`: Skala 1-5 (int)
- `Akt_Fisik`: Jam aktivitas fisik per hari (float)
- `Akt_Akademik`: Jam aktivitas akademik per hari (float)
- `Akt_NonAkademik`: Jam aktivitas non-akademik per hari (float)
- `Rasa_Lelah`: Skala 1-5 (int)
- `Rasa_Stress`: Skala 1-5 (int)
- `Sulit_Fokus`: Skala 1-5 (int)
- `Hilang_Minat`: Skala 1-5 (int)

## Penggunaan

1. **Isi Kuesioner**: Jawab 11 pertanyaan tentang kondisi kesehatan mental
2. **Lihat Hasil**: Sistem akan menampilkan klaster prediksi dengan visualisasi
3. **Baca Rekomendasi**: Ikuti saran yang diberikan berdasarkan hasil prediksi
4. **Cetak/Simpan**: Gunakan fitur cetak untuk menyimpan hasil

## Teknologi

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn (K-Means)
- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **Visualisasi**: Chart.js
- **Data Processing**: pandas, numpy

## Catatan Penting

- Aplikasi ini hanya untuk tujuan skrining awal, bukan diagnosis medis
- Untuk masalah kesehatan mental serius, konsultasikan dengan profesional
- Model dilatih berdasarkan data yang tersedia dan mungkin perlu update berkala
