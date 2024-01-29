from src.client.client import process_frame_array
from multiprocessing import Queue, Value
from unittest.mock import Mock
from ctypes import c_int

def test_process_frame_array(mocker):
    # Given...
    q = Queue()
    q.put(1)
    e = Mock()
    e.is_set.side_effect = [False, True]
    x = Value(c_int, 0)
    y = Value(c_int, 0)
    i = Value(c_int, 0)
    mocker.patch("src.client.client.process_image",
                 return_value=[5, 5])

    # When...
    process_frame_array(q, e, x, y, i)
    expected_x = 5
    expected_y = 5
    expected_i = 1

    # Then...
    assert x.value == expected_x
    assert y.value == expected_y
    assert i.value == expected_i