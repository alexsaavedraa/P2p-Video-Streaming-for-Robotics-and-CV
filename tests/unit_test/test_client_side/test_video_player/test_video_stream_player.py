from src.client.video_player import VideoStreamPlayer, MediaStreamError
from av import VideoFrame
from unittest.mock import Mock, MagicMock, AsyncMock
import pytest
from multiprocessing import Queue

@pytest.fixture()
def mock_player():
    title = "Test"
    q = MagicMock(Queue)
    player = VideoStreamPlayer(title, q)
    return player

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
    frame = MagicMock(VideoFrame)
    frame.to_rgb.return_value.to_ndarray.return_value = [1,1,1]
    mock_track = AsyncMock()
    mock_track.recv.side_effect=[frame, 
                                 MediaStreamError()]
    mock_player.addTrack(mock_track)
    mock_player.image_queue = Queue()
    
    
    mock_cv2 = mocker.patch("src.client.video_player.cv2")

    # When...
    await mock_player.run_track()
    expected_array =  [1,1,1]

    # Then...
    mock_cv2.imshow.assert_called_with("Client: Received Ball Animation", expected_array)
    assert mock_player.image_queue.get() == expected_array