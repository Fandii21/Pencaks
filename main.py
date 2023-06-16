from flask import Flask, render_template, request
import cv2
import time
import pickle
import numpy as np
import mediapipe as mp
from sklearn.preprocessing import LabelEncoder
import pandas as pd

app = Flask(__name__)

# Load model
with open("model/model.sav", "rb") as file:
    model = pickle.load(file)

# Load Silat dataset and label encoder
Silat = pd.read_csv("silat.csv")
label = Silat["classes"].unique()

label_encoder = LabelEncoder()
label_encoder.fit(label)

# Inisialisasi MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)


def preprocessing(pose_results):
    centering = np.array([])
    scaling = np.array([])
    body_keypoint_data = np.array([])

    # Centering coordinates Process
    for indexPoint in range(33):
        centering = np.append(
            centering,
            (
                pose_results.pose_landmarks.landmark[0].x
                - pose_results.pose_landmarks.landmark[indexPoint].x
            ),
        )
    for indexPoint in range(33):
        centering = np.append(
            centering,
            (
                pose_results.pose_landmarks.landmark[0].y
                - pose_results.pose_landmarks.landmark[indexPoint].y
            ),
        )
    for indexPoint in range(33):
        centering = np.append(
            centering,
            (
                pose_results.pose_landmarks.landmark[0].z
                - pose_results.pose_landmarks.landmark[indexPoint].z
            ),
        )
    centering = centering.reshape(3, 33)

    # Scaling
    for indexIter in range(3):
        for jointIter in range(33):
            scaling = np.append(
                scaling,
                centering[indexIter][jointIter]
                / np.max(np.absolute(centering[indexIter]))
                * 320,
            )

    # Normalization Process
    for jointIter in range(99):
        body_keypoint_data = np.append(body_keypoint_data, (scaling[jointIter] + 320))

    return body_keypoint_data


# Route untuk halaman utama
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/aithernals")
def aithernals():
    return render_template("aithernals.html")


@app.route("/sejarah_silat")
def sejarah_silat():
    return render_template("sejarah_silat.html")


@app.route("/gerakan_silat")
def gerakan_silat():
    return render_template("gerakan_silat.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/waktu_sehat")
def waktu_sehat():
    return render_template("waktu_sehat.html")


# Route untuk menerima dan memproses unggahan gambar
@app.route("/upload", methods=["POST"])
def upload():
    # Terima file gambar dari form
    image = request.files["file"]

    # Simpan gambar ke disk
    image.save("static/uploads/" + image.filename)

    # Baca gambar menggunakan OpenCV
    img = cv2.imread("static/uploads/" + image.filename)

    # Deteksi pose menggunakan MediaPipe
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        image_height, image_width, _ = img.shape
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Jika pose terdeteksi, lakukan prediksi
    if results.pose_landmarks:
        # Praproses pose menjadi fitur input
        body_keypoints = preprocessing(results)
        body_keypoints = np.expand_dims(body_keypoints, axis=0)
        predicted_class = label_encoder.inverse_transform(
            model.predict(body_keypoints)
        )[0]
    else:
        predicted_class = "Pose not detected"

    return render_template(
        "results.html", image=image.filename, predicted_class=predicted_class
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
