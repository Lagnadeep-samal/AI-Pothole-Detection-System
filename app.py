from flask import Flask, render_template, request
from ultralytics import YOLO
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load trained model
model = YOLO(
    r"D:/pothole-detection-system-using-convolution-neural-networks-master/runs/detect/train-4/weights/best.pt"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["image"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # YOLO Prediction
    results = model(
    filepath,
    conf=0.15,
    iou=0.20,
    imgsz=1280
)

    img = cv2.imread(filepath)

    minor = 0
    medium = 0
    major = 0

    for r in results:

        for box in r.boxes:

            conf = float(box.conf[0])

            cls = int(box.cls[0])

            label = model.names[cls]

            # -------------------------
            # Class-wise Confidence Filter
            # -------------------------

            if label == "minor_pothole" and conf < 0.55:
                continue

            if label == "medium_pothole" and conf < 0.45:
                continue

            if label == "major_pothole" and conf < 0.40:
                continue

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # Minor
            if label == "minor_pothole":

                minor += 1

                color = (0, 255, 0)

            # Medium
            elif label == "medium_pothole":

                medium += 1

                color = (0, 255, 255)

            # Major
            else:

                major += 1

                color = (0, 0, 255)

            # Draw Bounding Box Only
            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                color,
                3
            )

    # Road Score
    road_score = (
        minor +
        (medium * 2) +
        (major * 3)
    )

    # Road Condition
    if road_score <= 3:

        road_condition = "Good"

    elif road_score <= 8:

        road_condition = "Moderate"

    else:

        road_condition = "Poor"

    # Save Result Image
    cv2.imwrite(
        "static/result.jpg",
        img
    )

    return render_template(
        "index.html",
        minor=minor,
        medium=medium,
        major=major,
        road_score=road_score,
        road_condition=road_condition,
        image="result.jpg"
    )


if __name__ == "__main__":
    app.run(debug=True)