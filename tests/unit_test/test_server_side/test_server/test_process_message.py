from src import server
from unittest.mock import Mock

def test_process_message(mocker):
    # Given...
    message = "2,0,0"
    track = Mock()
    track.frame_dict = {0: [3, 4]}
    mock_display = mocker.patch("src.server.server.display_error")

    # When...
    server.server.process_message(message, track)
    expected_p1 = [3, 4]
    expected_p2 = [0, 0]
    expected_e = 5

    # Then...
    mock_display.assert_called_with(expected_p1,
                                    expected_p2,
                                    expected_e)
    
def test_process_message_exception(mocker):
    # Given...
    message = "2,0,0"
    track = Mock()
    track.frame_dict = {0: [3, 4]}
    mock_display = mocker.patch("src.server.server.display_error")
    mock_display.side_effect = Exception()

    # When...
    server.server.process_message(message, track)
    
    # Then passes