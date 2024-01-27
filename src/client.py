from aiortc.contrib.signaling import TcpSocketSignaling
from aiortc import (RTCPeerConnection, 
                    VideoStreamTrack)
import asyncio

HOST = "127.0. 0.1"
PORT = 8080

async def run_client(signaling, pc):
    obj = await signaling.recieve()
    return obj

if __name__ == "__main__":
    print("Initializing Server...")
    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    pc = RTCPeerConnection()
    loop = asyncio.get_event_loop()
    obj = loop.run_until_complete(
        run_client(
            signaling, 
            pc
        )
    )
    print(obj)