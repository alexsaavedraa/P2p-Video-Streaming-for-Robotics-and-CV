import cv2
import numpy as np
import pytest
from src.client.client import process_image

@pytest.fixture()
def mock_circle_image():
    img = np.zeros((30, 30, 3), dtype='uint8')
    cv2.circle(img, (15, 15), 10, (254, 254, 254), -1)
    return img

def test_process_imagee(mocker, mock_circle_image):
    # Given...
    mock_detector = mocker.patch("cv2.HoughCircles")
    mock_detector.return_value = [[[15, 15, 5]]]

    # When...
    actual_a, actual_b, actual_r = process_image(mock_circle_image)
    expected_a, expected_b, expected_r = [15, 15, 5]

    # Then...
    assert actual_a == expected_a
    assert actual_b == expected_b
    assert actual_r == expected_r
