# 🔥 Fire & Smoke Detection System — PKL KOM1399

Proyek ini dikembangkan sebagai bagian dari kegiatan **Praktik Kerja Lapangan (PKL) KOM1399 — Program Studi Ilmu Komputer IPB University**. Sistem ini menerapkan teknologi **Computer Vision dan Deep Learning** untuk mendeteksi **api (fire)** dan **asap (smoke)** secara **real-time** dari kamera **CCTV** maupun sumber video lainnya.

Tujuan utama sistem adalah memberikan **peringatan dini terhadap potensi kebakaran** sehingga penanganan dapat dilakukan lebih cepat untuk meminimalkan risiko kerugian material maupun korban jiwa.

---

## 🚀 Latar Belakang

Sistem monitoring CCTV tradisional masih bergantung pada pengawasan manual oleh operator, sehingga potensi kebakaran sering terlambat terpantau. Teknologi pendeteksian otomatis berbasis AI dapat membantu:

* Mendeteksi api & asap lebih cepat sejak fase awal kebakaran
* Mendukung kerja operator ruang kontrol
* Mengoptimalkan sistem keamanan kota berbasis **Smart City**

Proyek ini menjadi prototype sistem **Smart CCTV Fire Monitoring** yang dapat terintegrasi dengan jaringan CCTV pemerintah.

---

## 🧠 Teknologi yang Digunakan

| Komponen            | Teknologi                      |
| ------------------- | ------------------------------ |
| Bahasa Pemrograman  | Python                         |
| Model Deep Learning | YOLOv8 (Ultralytics)           |
| Framework CV        | OpenCV                         |
| GPU Training        | NVIDIA Tesla T4 (Kaggle)       |
| Tools Dataset       | Roboflow                       |
| Lingkungan Training | Google Colab / Kaggle Notebook |

---

## 📂 Dataset & Pelatihan Model

Dataset proyek terdiri dari:

* Cuplikan CCTV kota Bogor (berbagai waktu & cuaca)
* Video kebakaran kendaraan, bangunan, dan outdoor
* Augmentasi data untuk meningkatkan variasi

Kelas dataset:

| Label | Deskripsi                                                                                   |
| ----- | ------------------------------------------------------------------------------------------- |
| fire  | Api                                                                                         |
| smoke | Asap                                                                                        |
| other | Objek tidak berbahaya / pemicu false positive (lampu, cahaya, flare, kendaraan terang, dll) |

Model dilatih dalam **3 skenario baseline** untuk membandingkan pengaruh jumlah dataset **(2250 → 3300 → 4200 gambar)**.

---

## 📈 Hasil Evaluasi Model

Evaluasi menunjukkan bahwa performa **meningkat seiring bertambahnya keragaman dan ukuran dataset**.
Model terbaik adalah **Baseline 3 (4200 data)**.

| Model                   | Dataset    | Precision      | Recall         | mAP50          | mAP50-95       |
| ----------------------- | ---------- | -------------- | -------------- | -------------- | -------------- |
| Baseline 1              | 2250       | 0.755144       | 0.726539       | 0.809472       | 0.627858       |
| Baseline 2              | 3300       | 0.823709       | 0.817046       | 0.883189       | 0.697535       |
| ⭐ **Baseline 3 (Best)** | ⭐ **4200** | ⭐ **0.836449** | ⭐ **0.815056** | ⭐ **0.882227** | ⭐ **0.683106** |

🔍 **Analisis:**

* Baseline 3 mencapai performa tertinggi di seluruh metrik utama.
* Penambahan kelas **other** efektif mengurangi *false positive* (misal cahaya lampu, lampu kendaraan, flare).
* Model final mampu mengenali api & asap di berbagai kondisi lingkungan real seperti **lalu lintas padat, hujan, silau matahari, dan artefak kompresi CCTV**.
* Model Baseline 3 dipilih sebagai **model final implementasi real-time**.

---

## 🎥 Demo Hasil Deteksi

Video inferensi dapat dilihat melalui link berikut:
🔗 **[https://drive.google.com/xxxxxxxx](https://drive.google.com/xxxxxxxx)**

Visualisasi bounding box:

| Kelas    | Warna |
| -------- | ----- |
| 🔥 Fire  | Merah |
| 💨 Smoke | Ungu  |
| 🟢 Other | Hijau |

---

## 🖥 Cara Menjalankan Sistem

### 1️⃣ Install dependencies

```bash
pip install ultralytics opencv-python numpy
```

### 2️⃣ Load model

```python
from ultralytics import YOLO
model = YOLO("bestbaseline.pt")
```

### 3️⃣ Jalankan deteksi video / CCTV

```bash
python stream_test.py
```

---

## 🏗 Arsitektur Sistem

```
CCTV Stream / Video
        ↓
Frame Extraction
        ↓
YOLOv8 Inference (Fire / Smoke / Other)
        ↓
Bounding Box + Confidence + Warning Output
```

---

## 🔮 Future Development

| Rencana                                                | Status |
| ------------------------------------------------------ | ------ |
| Notifikasi Telegram/WhatsApp                           | 🔜     |
| Integrasi Dashboard Smart City                         | 🔜     |
| Multi-CCTV Streaming                                   | 🔜     |
| Perhitungan luas area api (fire severity)              | 🔜     |
| Early-fire prediction berbasis suhu & cuaca (IoT + AI) | 🔜     |

---

## 👩‍💻 Tentang Pengembang

Proyek dikembangkan oleh:
**Qonita Khairunissa — G6401221116**
Praktik Kerja Lapangan (PKL) — **Dinas Komunikasi dan Informatika Kota Bogor**
Periode: **2025**

> Sistem ini menjadi penerapan nyata ilmu *Computer Vision* dan *Deep Learning* untuk mendukung keamanan kota berbasis teknologi.

---

### ⭐ Dukungan

Jika repo ini bermanfaat, bantu dengan memberi ⭐ pada GitHub — sangat berarti untuk dokumentasi PKL & portofolio karier.

---

Kalau mau, aku bisa:
📌 tambahkan **screenshots bounding box ke README**
📌 buat **diagram arsitektur PNG**
📌 buat **badge spesifikasi model (GPU, Python, mAP)**
📌 atau **optimalkan README jadi bilingual (ID + EN)**

Tinggal bilang ya Bintang 💙

Dataset : https://app.roboflow.com/ds/PGJpht0h6q?key=jxqMN2BbWc
