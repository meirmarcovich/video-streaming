import queue
import pytest
import cv2
import numpy as np
from src.presenter import presenter, draw_bounding_boxes

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
    presenter(detection_queue)

    # Ensure draw_bounding_boxes() was called once with the correct arguments
    mock_draw.assert_called_with(frame, detections)

    print("Test passed: Presenter correctly overlays three bounding boxes.")
