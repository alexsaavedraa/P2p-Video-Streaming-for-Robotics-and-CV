from aiortc.contrib.signaling import TcpSocketSignaling
from aiortc import RTCPeerConnection
import asyncio
import socket

HOST = "127.0.0.1"
PORT = 8080

async def run_client(signaling):
    obj = await signaling.receive()
    print(obj)

if __name__ == "__main__":
    print("Initializing Client...")
    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run_client(
            signaling, 
        )
    )
