import cv2

def draw_bounding_boxes(frame, detections):
    for (x, y, w, h) in detections:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

def presenter(detection_queue):
    print("Presenter started, waiting for frames...")

    while True:
        data = detection_queue.get()
        if data is None:
            break

        frame, detections = data
        draw_bounding_boxes(frame, detections)

        cv2.imshow("Video Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    print("Presenter finished processing.")
