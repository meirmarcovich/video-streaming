import sys
import os
import queue
import pytest
from src.streamer import streamer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_streamer_sends_frames():
    video_path = "tests/SampleVideo_1280x720_2mb.mp4"
    frame_queue = queue.Queue() 

    streamer(video_path, frame_queue)

    if frame_queue.empty():
        pytest.fail("Streamer did not send any frames!")
