from aiortc.contrib.signaling import TcpSocketSignaling, BYE
from aiortc import (RTCPeerConnection, 
                    VideoStreamTrack)
import asyncio

HOST = "127.0.0.1"
PORT = 1234



async def run_server(signaling, pc):
    await signaling.connect()
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)
    while True:
        obj = await signaling.receive()
        if obj is BYE:
            print("Exiting")
            break

if __name__ == "__main__":
    print("Initializing Server...")
    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    pc = RTCPeerConnection()
    track = VideoStreamTrack()
    pc.addTrack(track)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run_server(
                signaling, 
                pc
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        # cleanup
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())