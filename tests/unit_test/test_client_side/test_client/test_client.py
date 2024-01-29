from src.client.client import run_client
from aiortc.contrib.signaling import BYE
from aiortc import RTCSessionDescription
from unittest.mock import Mock, AsyncMock, call
import pytest

@pytest.mark.asyncio
async def test_run_server():
    # Given...
    mock_signaling = AsyncMock()
    mock_signaling.receive.configure_mock(side_effect=[RTCSessionDescription("test", "offer"),
                                                       BYE])
    mock_pc = AsyncMock()
    mock_player = AsyncMock()
    mock_pc.on = Mock()

    # When...
    await run_client(mock_signaling,
                     mock_pc,
                     mock_player)

    # Then...
    mock_signaling.receive.assert_has_calls([call(), call()])
    mock_pc.setRemoteDescription.assert_called_once()