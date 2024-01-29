from src.client.video_player import VideoStreamPlayer, MediaStreamError
from unittest.mock import Mock, AsyncMock
import pytest
import asyncio

@pytest.fixture()
def mock_player():
    title = "Test"
    q = Mock("queue")
    return VideoStreamPlayer(title, q)

def test_init():
    # Given...
    title = "Test"
    q = Mock("queue")

    # When...
    player = VideoStreamPlayer(title, q)

    # Then...
    assert player.title == title
    assert player.image_queue == q

def test_addTrack(mock_player):
    # Given...
    track = Mock("track")

    # When...
    mock_player.addTrack(track)

    # Then...
    assert mock_player.track == track

@pytest.mark.asyncio
async def test_start(mocker, mock_player):
    # Given...
    mock_asyncio = mocker.patch("src.client.video_player.asyncio")

    # When...
    await mock_player.start()

    # Then...
    mock_asyncio.ensure_future.assert_called_once()

@pytest.mark.asyncio
async def test_stop(mocker, mock_player):
    # Given...
    mock_cv2 = mocker.patch("src.client.video_player.cv2")

    # When...
    await mock_player.stop()

    # Then...
    mock_cv2.destroyAllWindows.assert_called_once()

@pytest.mark.asyncio
async def test_run_track(mocker, mock_player):
    # Given...
    mock_track = mocker.patch("src.client.video_player.MediaStreamTrack")
    mock_recv = mocker.patch("src.client.video_player.MediaStreamTrack.recv")
    mock_track.recv = mock_recv
    mock_player.addTrack(mock_track)
    frame = Mock("frame")
    mock_recv.configure_mock(side_effect=[asyncio.Future().set_result(frame), MediaStreamError()])
    mock_cv2 = mocker.patch("src.client.video_player.cv2")

    # When...
    await mock_player.run_track()
    expected_array = frame.to_rgb.return_value.to_ndarray.return_value
    # Then...
    mock_cv2.imshow.assert_called_with("Client: Received Ball Animation", expected_array)
    mock_player.image_queue.put.assert_called_with(expected_array)