import cv2
import time

def streamer(video_path, frame_queue):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        frame_queue.put(None)  # Ensure detector doesn't wait forever
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS if unknown
    frame_time = 1.0 / fps  # Calculate time per frame

    print(f"Streaming video at {fps:.2f} FPS")

    while cap.isOpened():
        start_time = time.time()  # Track when frame is read

        ret, frame = cap.read()
        if not ret:
            break

        frame_queue.put(frame)

        # Control playback speed based on real FPS
        elapsed_time = time.time() - start_time
        remaining_time = frame_time - elapsed_time

        if remaining_time > 0:
            time.sleep(remaining_time)

    frame_queue.put(None)  # Signal end of stream
    cap.release()
    print("Streamer finished.")
