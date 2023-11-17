from flask import Flask, jsonify
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

@app.route('/process_video')
def process_video():
    # Example video file (you need to replace this with your actual video file)
    video_file = 'path_to_your_video.mp4'

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return jsonify({"error": "Failed to open video file."})

    # Initialize mediapipe components
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    # Process first frame of the video
    ret, frame = cap.read()
    if not ret:
        return jsonify({"error": "Failed to read video frame."})

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        frame = cv2.resize(frame, (640, 640))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        # Convert image to JPEG format for easy display in response
        _, jpeg_image = cv2.imencode('.jpg', image)
        response_image = jpeg_image.tobytes()

    cap.release()

    # Return the processed image in response (as binary data)
    return response_image, 200, {'Content-Type': 'image/jpeg'}

if __name__ == '__main__':
    app.run(debug=True)
