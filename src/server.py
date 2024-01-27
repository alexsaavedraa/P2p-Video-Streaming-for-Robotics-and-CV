from aiortc.contrib.signaling import TcpSocketSignaling
from aiortc import (RTCPeerConnection, 
                    VideoStreamTrack)
import asyncio
import socket

HOST = "127.0.0.1"
PORT = 8080

async def run_server(signaling, pc):
    await signaling.connect()
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)

if __name__ == "__main__":
    print("Initializing Server...")
    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    pc = RTCPeerConnection()
    loop = asyncio.get_event_loop()
    track = VideoStreamTrack()
    pc.addTrack(track)
    loop.run_until_complete(
        run_server(
            signaling, 
            pc
        )
    )