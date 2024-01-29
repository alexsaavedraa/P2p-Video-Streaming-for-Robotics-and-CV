# from src.client import (process_frame_array,
#                         process_images,
#                         run_client)
# import pytest
# from unittest.mock import Mock
# from ctypes import c_int
# from multiprocessing import (Queue, Value, Event)

# @pytest.fixture
# def mock_process_images(mocker):
#     mocker.patch('process_images', return_value=(1, 2))

# @pytest.fixture
# def mock_event(mocker):
#     mocker.patch('Event.is_set', return_value=(1, 2))

# def test_process_frame_array():
#     # given...
#     queue = Queue()
#     termination_event = Mock()
#     x = Value(c_int, 0)
#     y = Value(c_int, 0)
#     i = Value(c_int, 0)
    
#     # when...


#     # then...
#     assert True