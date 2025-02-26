import queue
import pytest
import cv2
import numpy as np
from src.detector import detector

def run_detector_with_frames(frames):
    """Helper function to send frames to detector and return results."""
    frame_queue = queue.Queue()
    detection_queue = queue.Queue()

    for frame in frames:
        frame_queue.put(frame)
    
    frame_queue.put(None)  # End signal

    detector(frame_queue, detection_queue)

    results = []
    while not detection_queue.empty():
        results.append(detection_queue.get(timeout=3))

    return results

def test_detector_processes_single_frame():
    print("Starting test: detector should process a single blank frame with no detections.")
    blank_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    results = run_detector_with_frames([blank_frame])

    assert isinstance(results[0], tuple), "Detector should return a tuple (frame, detections)."
    assert isinstance(results[0][0], np.ndarray), "First element should be a frame (numpy array)."
    assert isinstance(results[0][1], list), "Second element should be a list of detections."
    assert len(results[0][1]) == 0, "Detector should return an empty list when there is no motion."
    assert results[-1] is None, "Detector should send None as an end signal."

    print("Test passed: Detector handles empty frames correctly.")

def test_detector_processes_multiple_identical_frames():
    print("Starting test: detector should process multiple identical frames without detections.")
    blank_frame = np.zeros((720, 1280, 3), dtype=np.uint8)

    results = run_detector_with_frames([blank_frame] * 5)

    for result in results[:-1]:  # Exclude the final None signal
        assert isinstance(result, tuple), "Detector should return a tuple (frame, detections)."
        assert isinstance(result[0], np.ndarray), "First element should be a frame (numpy array)."
        assert isinstance(result[1], list), "Second element should be a list of detections."
        assert len(result[1]) == 0, "Detector should return an empty list when there is no motion."

    print("Test passed: Detector handles multiple identical frames correctly.")

def test_detector_detects_motion():
    print("Starting test: detector should detect motion.")
    blank_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    moving_frame = blank_frame.copy()
    cv2.rectangle(moving_frame, (300, 300), (400, 400), (255, 255, 255), -1)

    results = run_detector_with_frames([blank_frame, moving_frame])

    assert isinstance(results[0][1], list), "First frame should have an empty detections list."
    assert len(results[0][1]) == 0, "First frame should not detect motion."
    assert isinstance(results[1][1], list), "Second frame should have a detections list."
    assert len(results[1][1]) > 0, "Detector should detect at least one object in the second frame."

    for bbox in results[1][1]:
        assert isinstance(bbox, tuple) and len(bbox) == 4, "Each detection should be a bounding box (x, y, w, h)."

    print("Test passed: Detector correctly detects motion in the second frame.")
