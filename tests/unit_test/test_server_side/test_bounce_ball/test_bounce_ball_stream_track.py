from src.server.bounce_ball import BounceBallStreamTrack
from unittest.mock import Mock
import pytest

def test_get_next_frame_x_hit_480():
    # Given...
    stream = BounceBallStreamTrack()
    stream.ball.x = 455
    
    # When...
    stream.get_next_frame()
    expected_dx = -5

    # Then...
    assert stream.dx == expected_dx

def test_get_next_frame_x_hit_0():
    # Given...
    stream = BounceBallStreamTrack()
    stream.ball.x = 25
    stream.dx = -5
    
    # When...
    stream.get_next_frame()
    expected_dx = 5

    # Then...
    assert stream.dx == expected_dx

def test_get_next_frame_y_hit_640():
    # Given...
    stream = BounceBallStreamTrack()
    stream.ball.y = 615
    stream.dy = 5
    
    # When...
    stream.get_next_frame()
    expected_dy = -5

    # Then...
    print(stream.ball.x, stream.ball.y)
    assert stream.dy == expected_dy

def test_get_next_frame_y_hit_0():
    # Given...
    stream = BounceBallStreamTrack()
    stream.ball.y = 25
    stream.dy = -5
    
    # When...
    stream.get_next_frame()
    expected_dy = 5

    # Then...
    assert stream.dy == expected_dy

@pytest.mark.asyncio
async def test_recv(mocker):
    # Given...
    stream = BounceBallStreamTrack()
    stream.get_next_frame = Mock()
    stream.get_next_frame.return_value = Mock()
    mock_timestamp = mocker.patch('src.server.bounce_ball.BounceBallStreamTrack.next_timestamp')
    mock_timestamp.configure_mock(return_value=("pts", "time"))
    
    # When...
    actual = await stream.recv()
    expected_pts = "pts"
    expected_time = "time"
    expected_x = 100
    expected_y = 100

    # Then...
    assert actual.pts == expected_pts
    assert actual.time_base == expected_time
    assert stream.counter == 1
    assert stream.frame_dict == {0: [expected_x, expected_y]}