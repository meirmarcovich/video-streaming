import queue
import pytest
import cv2
import numpy as np
from unittest.mock import patch
from src.presenter import presenter, draw_bounding_boxes, draw_timestamp

@pytest.fixture
def mock_cv2(mocker):
    """Mock OpenCV functions to avoid opening windows and requiring user input."""
    mocker.patch("cv2.imshow")
    mocker.patch("cv2.waitKey", return_value=ord('q'))  # Simulate pressing 'q'

def test_presenter_draws_three_bounding_boxes(mock_cv2, mocker):
    print("Starting test: Presenter should draw three bounding boxes.")

    frame = np.zeros((720, 1280, 3), dtype=np.uint8)

    # Define three sample detections [(x, y, w, h)]
    detections = [
        (50, 50, 30, 30),
        (200, 200, 60, 60),
        (400, 400, 90, 90)
    ]

    detection_queue = queue.Queue()
    detection_queue.put((frame, detections))
    detection_queue.put(None)  # End signal

    # Mock draw_bounding_boxes to track calls
    mock_draw = mocker.patch("src.presenter.draw_bounding_boxes")

    print("Running presenter function...")
    presenter(detection_queue, fps=30)  # ✅ Fix: Pass FPS

    # Ensure draw_bounding_boxes() was called once with the correct arguments
    mock_draw.assert_called_with(frame, detections)

    print("Test passed: Presenter correctly overlays three bounding boxes.")

# ✅ New test for timestamp
def test_draw_timestamp(mocker):
    print("Starting test: Timestamp should be drawn correctly.")

    frame = np.zeros((720, 1280, 3), dtype=np.uint8)  # Blank frame
    frame_index = 300  # 10 seconds into the video at 30 FPS
    fps = 30

    mock_putText = mocker.patch("cv2.putText")

    draw_timestamp(frame, frame_index, fps)

    expected_time_str = "00:10"  # Expected MM:SS format

    # Verify if putText was called with the correct time string
    mock_putText.assert_called_with(frame, expected_time_str, (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    print("Test passed: Clock is correctly drawn.")
