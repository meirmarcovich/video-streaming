import multiprocessing
import queue
import cv2
import time
from src.streamer import streamer
from src.detector import detector
from src.presenter import presenter

def main(video_path):
    print("Starting Video Processing Pipeline...")

    frame_queue = multiprocessing.Queue()
    detection_queue = multiprocessing.Queue()

    streamer_process = multiprocessing.Process(target=streamer, args=(video_path, frame_queue))
    detector_process = multiprocessing.Process(target=detector, args=(frame_queue, detection_queue))
    presenter_process = multiprocessing.Process(target=presenter, args=(detection_queue,))

    streamer_process.start()
    detector_process.start()
    presenter_process.start()

    streamer_process.join()
    detector_process.join()
    presenter_process.join()

    print("Video Processing Pipeline Completed.")

if __name__ == "__main__":
    video_path = "tests/SampleVideo_1280x720_2mb.mp4"  # Adjust path if needed
    main(video_path)
