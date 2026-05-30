from ultralytics import YOLO

# Load trained model
model = YOLO(
    r"D:/pothole-detection-system-using-convolution-neural-networks-master/runs/detect/train-4/weights/best.pt"
)

# Predict
results = model(
    r"D:/pothole-detection-system-using-convolution-neural-networks-master/My Dataset/test/images",
    conf=0.40,
    iou=0.25,
         # NMS threshold
    imgsz=960,      # Larger image size for small potholes
    save=True,
    save_txt=True
)

# Display results
for r in results:
    print("\nImage:", r.path)

    if len(r.boxes) == 0:
        print("No pothole detected")

    for box in r.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        print(
            f"Detected: {model.names[cls]} | Confidence: {conf:.2f}"
        )