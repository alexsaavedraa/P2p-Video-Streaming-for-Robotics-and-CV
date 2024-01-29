from src.server.server import run_server
from aiortc.contrib.signaling import BYE
from aiortc import RTCSessionDescription
from unittest.mock import Mock, AsyncMock
import pytest

@pytest.mark.asyncio
async def test_run_server(mocker):
    # Given...
    mock_signaling = AsyncMock()
    mock_signaling.receive.configure_mock(side_effect=[RTCSessionDescription("test", "offer"),
                                                       BYE])
    mock_pc = AsyncMock()
    mock_track = AsyncMock()
    mock_channel = AsyncMock()
    mock_channel.on = Mock()
    # mock_on_message = mocker.patch("src.server.server.on_message")
    # When...
    await run_server(mock_signaling,
                     mock_pc,
                     mock_track,
                     mock_channel)

    # Then...
    mock_signaling.connect.assert_called_once()
    mock_pc.setRemoteDescription.assert_called_once()