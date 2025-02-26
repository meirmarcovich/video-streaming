import cv2

def pre_process_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def initialize_background_subtractor(frame):
    fgbg = cv2.createBackgroundSubtractorMOG2()
    fgbg.apply(pre_process_frame(frame))
    return fgbg

def detect_motion(frame, fgbg):
    fgmask = fgbg.apply(pre_process_frame(frame))
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [cv2.boundingRect(cnt) for cnt in contours if cv2.contourArea(cnt) > 100]

def detector(frame_queue, detection_queue):
    print("Detector started, waiting for frames...")
    
    first_frame = frame_queue.get()
    if first_frame is None:
        print("No frames received. Exiting detector...")
        detection_queue.put(None)
        return
    
    detection_queue.put((first_frame, []))
    fgbg = initialize_background_subtractor(first_frame)
    
    while True:
        frame = frame_queue.get()
        if frame is None:
            print("Received stop signal, exiting detector...")
            break

        print("Processing frame...")
        detections = detect_motion(frame, fgbg)
        print(f"Detected {len(detections)} moving objects.")
        detection_queue.put((frame, detections))

    print("Detector finished processing.")
    detection_queue.put(None)
