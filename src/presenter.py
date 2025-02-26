import cv2
import time

def draw_bounding_boxes(frame, detections):
    for (x, y, w, h) in detections:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

def draw_timestamp(frame, frame_index, fps):
    video_time = frame_index / fps
    minutes = int(video_time // 60)
    seconds = int(video_time % 60)
    time_str = f"{minutes:02}:{seconds:02}"  # Format as MM:SS
    cv2.putText(frame, time_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

def presenter(detection_queue, fps):
    print("Presenter started, waiting for frames...")
    frame_index = 0
    frame_duration = 1.0 / fps  # Calculate expected frame duration

    while True:
        start_time = time.time()  # Track when we start processing a frame

        data = detection_queue.get()
        if data is None:
            print("Received stop signal, exiting presenter...")
            break

        frame, detections = data
        draw_bounding_boxes(frame, detections)
        draw_timestamp(frame, frame_index, fps)

        cv2.imshow("Video Stream", frame)
        frame_index += 1  # Increment frame index

        elapsed_time = time.time() - start_time
        remaining_time = frame_duration - elapsed_time

        if remaining_time > 0:
            time.sleep(remaining_time)  # Ensure frames are displayed at correct speed

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    print("Presenter finished processing.")
