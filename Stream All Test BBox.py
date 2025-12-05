from ultralytics import YOLO
import cv2
import requests
import os
import time

# ========================
#  Load YOLOv8 Model
# ========================
model_path = "C:/Users/qonit/Documents/A. Magang/A. Dokumentasi/Code VS/bestbaseline4.pt"
model = YOLO(model_path)

# ========================
#  Class & Color Config
# ========================
classNames = ["fire", "other", "smoke"]
color_map = {
    "fire": (0, 0, 255),       # merah
    "other": (0, 255, 0),      # hijau
    "smoke": (128, 0, 128)     # ungu
}

# ========================
#  CCTV List
# ========================

# Daftar CCTV (stream_url + label lokasi)
cctv_list = [
    {
        "id": "CCTV JALAN SUKASARI",
        "url": "https://restreamer3.kotabogor.go.id/memfs/0ec104af-9036-48db-b643-ced9d1d42c21.m3u8"
    },
    {
        "id": "CCTV GANG AUT",
        "url": "https://restreamer2.kotabogor.go.id/memfs/64b180ce-d237-44d9-b857-c610e1d0c75c.m3u8"
    },
    {
        "id": "CCTV KAPTEN MUSLIHAT",
        "url": "https://restreamer2.kotabogor.go.id/memfs/3ec6eaf2-4da1-4adb-8c15-0251e69121d6.m3u8"
    },
    {
        "id": "CCTV LAWANG GINTUNG",
        "url": "https://restreamer2.kotabogor.go.id/memfs/04d5f235-00ce-4c57-ae9a-09214c688086.m3u8"
    },
    {
        "id": "CCTV MAYOR OKING",
        "url": "https://restreamer2.kotabogor.go.id/memfs/a3d87684-2cdd-4190-ac07-8b915864daef.m3u8"
    },
    {
        "id": "CCTV TUGU KUJANG",
        "url": "https://restreamer2.kotabogor.go.id/memfs/5a5cf878-9d9b-4400-a73a-27a5b24a6ec4.m3u8"
    },
    {
        "id": "CCTV CIHELEUT",
        "url": "https://restreamer2.kotabogor.go.id/memfs/f5ca1d37-c267-4806-850b-d1ca537fb29a.m3u8"
    },
    {
        "id": "CCTV SIMPANG BTM",
        "url": "https://restreamer2.kotabogor.go.id/memfs/f707b72a-5c95-421a-9f3a-2e478794bd76.m3u8"
    },
    {
        "id": "CCTV DEPAN ALUN-ALUN",
        "url": "https://restreamer2.kotabogor.go.id/memfs/c07c1926-288c-46e4-a19c-9f51022edc5d.m3u8"
    },
    {
        "id": "CCTV PASAR BOGOR",
        "url": "https://restreamer2.kotabogor.go.id/memfs/b43066d4-b1e4-4e90-8e17-86c15a9a944e.m3u8"
    },
    {
        "id": "CCTV DEPAN KANTOR DISHUB KOTA BOGOR",
        "url": "https://restreamer2.kotabogor.go.id/memfs/0518012b-655d-4a7d-83d6-b7bb1faf4396.m3u8"
    },
    {
        "id": "CCTV JUANDA",
        "url": "https://restreamer2.kotabogor.go.id/memfs/62cded1f-90d0-4af6-b330-dc40af5fdd67.m3u8"
    },
    {
        "id": "CCTV SEKETENG SURYAKENCANA",
        "url": "https://restreamer2.kotabogor.go.id/memfs/3d51d3a1-0d90-4230-956c-60dea3c11ac3.m3u8"
    },
    {
        "id": "CCTV OTISTA",
        "url": "https://restreamer2.kotabogor.go.id/memfs/b75e84e5-d033-48fb-aa67-fc48c5e11091.m3u8"
    },
    {
        "id": "CCTV SKETENG GUDANG",
        "url": "https://restreamer2.kotabogor.go.id/memfs/1083f9b4-b193-490d-aa45-31cbc69913fb.m3u"
    },
    {
        "id": "CCTV PEDATI ARAH GUDANG",
        "url": "https://restreamer3.kotabogor.go.id/memfs/c2d90a44-8f2c-4103-82ad-6cb1730a5000.m3u8"
    },
    {
        "id": "CCTV SIMPANG DEPOM",
        "url": "https://restreamer2.kotabogor.go.id/memfs/70d8b8dd-35ba-4895-8c03-8dbd306ce5cb.m3u8"
    },
    {
        "id": "CCTV ALUN-ALUN BRI 2",
        "url": "https://restreamer3.kotabogor.go.id/memfs/b99d528a-1eb8-47bf-ba0f-a63fe11dbece.m3u8"
    },
    {
        "id": "CCTV MASJID AGUNG",
        "url": "https://restreamer3.kotabogor.go.id/memfs/3cd8d68e-9022-4891-887b-3ff87fe12b56.m3u8"
    },
    {
        "id": "CCTV SUDIRMAN",
        "url": "https://restreamer3.kotabogor.go.id/memfs/3b76a9cd-0b52-42bd-8577-eb3ecb084ec3.m3u8"
    },
    {
        "id": "CCTV PEDATI SURYAKENCANA",
        "url": "https://restreamer3.kotabogor.go.id/memfs/eedbb9a2-1571-41bd-92db-73b946e3e9b2.m3u8"
    },
    {
        "id": "EMPANG ARAH PANCASAN",
        "url": "https://restreamer3.kotabogor.go.id/memfs/db8ddbdf-cd84-439b-b1fe-a283dffdd5b6.m3u8"
    },
    {
        "id": "CCTV ALUN-ALUN BRI 1",
        "url": "https://restreamer3.kotabogor.go.id/memfs/38611ade-09b7-4e5b-b835-f5c3a56bb373.m3u8"
    },
    {
        "id": "CCTV EMPANG ARAH BNR",
        "url": "https://restreamer3.kotabogor.go.id/memfs/ca848bb3-3f17-4cea-8bef-d89dd116fd7c.m3u8"
    },
    {
        "id": "CCTV LAWANG SEKETENG",
        "url": "https://restreamer3.kotabogor.go.id/memfs/f946ad94-d7c0-4bea-bb43-51adbdc90b95.m3u8"
    },
    {
        "id": "CCTV PEDATI LAWANG",
        "url": "https://restreamer3.kotabogor.go.id/memfs/3ec91e05-edf0-451f-b363-4b3c52b75805.m3u8"
    },
    {
        "id": "CCTV DEPAN MASJID RAYA",
        "url": "https://restreamer3.kotabogor.go.id/memfs/aff6fd2d-2f56-4072-b5c3-774f07722a04.m3u8"
    },
    {
        "id": "CCTV JEMBATAN MERAH",
        "url": "https://restreamer3.kotabogor.go.id/memfs/5f1e2a06-059c-4c00-9102-ceaf12e2b577.m3u8"
    },
    {
        "id": "CCTV PANCASAN",
        "url": "https://restreamer3.kotabogor.go.id/memfs/5c9ce5e6-4971-483f-914f-39ec33a7764e.m3u8"
    },
    {
        "id": "CCTV JUANDA ARAH SURKEN",
        "url": "https://restreamer3.kotabogor.go.id/memfs/f6b50f38-9184-418e-b3f9-05faaa9b387d.m3u8"
    },
    {
        "id": "CCTV JUANDA ARAH EMPANG",
        "url": "https://restreamer3.kotabogor.go.id/memfs/31b05614-19d8-492e-b244-903e8aa28292.m3u8"
    },
    {
        "id": "CCTV KOMINFO ARAH TAJUR",
        "url": "https://restreamer3.kotabogor.go.id/memfs/31970416-64db-400c-af8b-b929b673f7a5.m3u8"
    },
    {
        "id": "CCTV KOMINFO ARAH PUNCAK",
        "url": "https://restreamer3.kotabogor.go.id/f933d962-fa27-4ca0-a166-24a2e23896ad.html"
    },
    {
        "id": "CCTV KOMINFO PINTU 3",
        "url": "https://restreamer3.kotabogor.go.id/memfs/6542214a-fe60-4e0f-9330-79106c62ddcc.m3u8"
    },
    {
        "id": "CCTV SIMPANG DENPOM ARAH PINTU UTAMA ISTANA",
        "url": "https://restreamer3.kotabogor.go.id/memfs/67ebf216-fa63-4a6a-9ea8-1e5604257f74.m3u8"
    },
    {
        "id": "POMAD ARAH TANAH BARU",
        "url": "https://restreamer.kotabogor.go.id/memfs/caf65442-05fa-4fc9-a697-d49f4572ed62.m3u8"
    },
    {
        "id": "POMAD ARAH CILUAR",
        "url": "https://restreamer.kotabogor.go.id/memfs/8f296b5c-087d-415d-9360-d8c2c18e02b9.m3u8"
    },
    {
        "id": "MA SALMUN ARAH MAWAR",
        "url": "https://restreamer.kotabogor.go.id/memfs/aaa81ab7-5f96-4073-8090-e33d882a5dff.m3u8"
    },
    {
        "id": "MA SALMUN ARAH DEWI SARTIKA",
        "url": "https://restreamer.kotabogor.go.id/memfs/ee837053-a8e7-4fde-84ed-fc88ad26d3a5.m3u8"
    },
    {
        "id": "MA SALMUN ARAH JEMBATAN MERAH",
        "url": "https://restreamer.kotabogor.go.id/memfs/e7609045-eeaf-4579-8eca-fc3e61502eac.m3u8"
    },
    {
        "id": "MA SALMUN ARAH PS ANYAR",
        "url": "https://restreamer.kotabogor.go.id/memfs/8061c0e7-e3e6-4842-b80a-8e41dc7c127c.m3u8"
    },
    {
        "id": "TAMAN CORAT CORET",
        "url": "https://restreamer.kotabogor.go.id/memfs/d6ef0d86-68f1-42c9-acd7-667d05bfa463.m3u8"
    },
    {
        "id": "TAMAN CORAT CORET ARAH DISDUKCAPIL",
        "url": "https://restreamer.kotabogor.go.id/memfs/cdfdab2e-7f7d-4bd1-8a7a-698559837d91.m3u8"
    },
    {
        "id": "TAMAN EKSPRESI 1",
        "url": "https://restreamer.kotabogor.go.id/memfs/87ec2d37-4a67-4edf-a748-01e511f77585.m3u8"
    },
    {
        "id": "TAMAN EKSPRESI 2",
        "url": "https://restreamer.kotabogor.go.id/memfs/a5658165-b05c-4a10-a8ca-951551985530.m3u8"
    },
    {
        "id": "TAMAN SEMPUR 2",
        "url": "https://restreamer2.kotabogor.go.id/memfs/81d53543-1607-45df-9d17-db70c9960345.m3u8"
    },
    {
        "id": "POMAD ARAH BOGOR",
        "url": "https://restreamer.kotabogor.go.id/memfs/bb88ed9f-e6c6-433b-8f12-26c249e8e8f9.m3u8"
    }
]

# ========================
#  Folder Output
# ========================
save_frame_folder = "C:/Users/qonit/Documents/A. Magang/A. Dokumentasi/Code VS/detected_frames_bbl4noon"
save_video_folder = "C:/Users/qonit/Documents/A. Magang/A. Dokumentasi/Code VS/videos_bbl4noon"

os.makedirs(save_frame_folder, exist_ok=True)
os.makedirs(save_video_folder, exist_ok=True)

# ========================
#  Webhook Alert Function
# ========================
def trigger_alert(stream_id, label):
    webhook_url = 'https://labs-workflow.kotabogor.go.id/webhook/88864eb0-2dea-4d3c-b679-190eddd99d02'
    headers = {
        'x-api-key': 'NvCemDa4gLdJ4qZNQ5Ih',
        'Content-Type': 'application/json'
    }
    daftar_nomor = ['081326928422']
    isi_pesan = f"Deteksi {label} pada {stream_id}. Segera periksa lokasi!"

    data = {
        'daftarNomor': daftar_nomor,
        'isiPesan': isi_pesan
    }

    try:
        response = requests.post(webhook_url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Alert terkirim: {label} di {stream_id}")
    except requests.exceptions.RequestException as e:
        print(f"Gagal kirim alert: {e}")


# ========================
#  DETECTION PER CCTV
# ========================
alert_interval = 300  # 5 menit
last_alert_time = {}

for cctv in cctv_list:
    stream_id = cctv["id"]
    stream_url = cctv["url"]

    print(f"\nMemulai deteksi pada {stream_id}...")

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print(f"Tidak bisa membuka stream: {stream_id}")
        continue

    # Video output untuk lokasi ini
    output_path = f"{save_video_folder}/{stream_id.replace(' ', '_')}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (640, 480))

    frame_count = 0
    max_frames = 300
    last_alert_time[stream_id] = 0

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ Gagal mengambil frame dari {stream_id}")
            break

        # Resize biar stabil
        frame = cv2.resize(frame, (640, 480))

        # ===== YOLO DETECTION =====
        results = model(frame)

        detected_any = False  # Untuk simpan frame hanya jika ada deteksi

        for r in results:
            for box in r.boxes:
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = classNames[class_id]

                # threshold umum
                if confidence > 0.40:
                    detected_any = True

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    color = color_map.get(class_name, (255, 255, 255))
                    label = f"{class_name.upper()} {confidence:.2f}"

                    # Gambar bbox
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1 + 8, y1 - 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                    # === ALERT khusus fire ===
                    if class_name == "fire" and confidence > 0.90:
                        now = time.time()
                        if now - last_alert_time[stream_id] > alert_interval:
                            trigger_alert(stream_id, label)
                            last_alert_time[stream_id] = now

        # Simpan ke video
        out.write(frame)

        # Simpan frame hanya jika ada bbox
        if detected_any:
            cv2.imwrite(f"{save_frame_folder}/{stream_id.replace(' ', '_')}_frame_{frame_count}.jpg", frame)

        frame_count += 1

    print(f"✅ Selesai deteksi {stream_id}. Video & frame disimpan.")

    cap.release()
    out.release()

print("\nSemua CCTV selesai diproses.\n")
