from aiortc.contrib.signaling import TcpSocketSignaling, BYE
from aiortc import (RTCPeerConnection, 
                    VideoStreamTrack, RTCIceCandidate)
import asyncio
import socket
HOST = "127.0.0.1"
PORT = 1234
import numpy
import cv2
import math
from av import VideoFrame



async def run_server(signaling, pc):

    pc.addTrack(VideoStreamTrack())
    await signaling.connect()
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)
    while True:
        obj = await signaling.receive()
        if isinstance(obj, RTCIceCandidate):
            await pc.addIceCandidate(obj)
        elif obj is BYE:
            print("Exiting")
            break
    
    

        

if __name__ == "__main__":
    print("Initializing Server...")
    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    pc = RTCPeerConnection()
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