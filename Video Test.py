from ultralytics import YOLO
import cv2
import cvzone
import math
import os

print("Fire & Smoke Detection - Video Processing")
print("=" * 70)

# Setup paths
video_path = "C:/Users/qonit/Documents/A. Magang/A. Dokumentasi/Code VS/Data Vid/Rekaman_cctv_siang_202511291442_7tgn3.mp4"
model_path = "C:/Users/qonit/Documents/A. Magang/A. Dokumentasi/Code VS/bestbaseline4.pt"
output_path = "C:/Users/qonit/Documents/A. Magang/A. Dokumentasi/Code VS/Data Vid/output_bestbaseline4a.mp4"
save_frame_folder = "C:/Users/qonit/Documents/A. Magang/A. Dokumentasi/Code VS/Data Vid/detected_frames_bestbaseline4a"

os.makedirs(save_frame_folder, exist_ok=True)

# Load model
model = YOLO(model_path)
print(f"✅ Model loaded: {model_path}")

# Class names + colors
classNames = ["fire", "other", "smoke"]
color_map = {
    "fire": (0, 0, 255),       # merah
    "other": (0, 255, 0),      # hijau
    "smoke": (128, 0, 128)     # ungu
}

# Open video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("❌ Error: Cannot open video!")
    exit()

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"📹 Video info:")
print(f"   - Resolution: {width}x{height}")
print(f"   - FPS: {fps}")
print(f"   - Total frames: {total_frames}")

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

print(f"\nOutput will be saved to: {output_path}")
print("\nProcessing... (Press 'q' to stop)\n")

frame_count = 0
detection_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("\n✅ Video processing completed!")
        break

    frame_count += 1
    results = model(frame, stream=True, conf=0.3, iou=0.4)

    detected_any = False

    for info in results:
        boxes = info.boxes
        for box in boxes:
            confidence = float(box.conf[0])
            confidence_pct = math.ceil(confidence * 100)
            class_id = int(box.cls[0])

            if confidence_pct > 70:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                class_name = classNames[class_id]
                color = color_map.get(class_name, (255, 255, 255))  # fallback putih

                # Draw thin bbox (thickness=1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)

                # Clean label
                label = f"{class_name.upper()} {confidence_pct}%"

                # Text box like your second script
                cv2.putText(
                    frame, label, (x1 + 8, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (255, 255, 255), 2
                )

                detected_any = True
                detection_count += 1

    # Save frame if detection exists
    if detected_any:
        cv2.imwrite(
            f"{save_frame_folder}/frame_{frame_count}.jpg",
            frame
        )

    cv2.putText(frame, f"Frame: {frame_count}/{total_frames}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    out.write(frame)
    cv2.imshow("Fire & Smoke Detection", frame)

    if frame_count % 30 == 0:
        progress = (frame_count / total_frames) * 100
        print(f"Progress: {progress:.1f}% ({frame_count}/{total_frames}) - Detections: {detection_count}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n⚠️  Stopped by user")
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)
print(f"Total frames processed: {frame_count}")
print(f"Total detections: {detection_count}")
print(f"Frames saved to: {save_frame_folder}")
print(f"\n✅ Output saved: {output_path}")
print("=" * 70)
