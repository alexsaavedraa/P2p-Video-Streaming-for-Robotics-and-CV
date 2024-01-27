from aiortc.contrib.signaling import TcpSocketSignaling, BYE
from aiortc import (RTCPeerConnection, 
                    RTCSessionDescription)
from aiortc.contrib.media import MediaRecorder
import asyncio

HOST = "127.0.0.1"
PORT = 1234

async def run_client(signaling, pc, recorder):
    @pc.on("track")
    def on_track(track):
        print("Receiving %s" % track.kind)
        recorder.addTrack(track)

    while True:
        obj = await signaling.receive()
        if isinstance(obj, RTCSessionDescription):
                await pc.setRemoteDescription(obj)
                await recorder.start()
                if obj.type == "offer":
                    await pc.setLocalDescription(await pc.createAnswer())
                    await signaling.send(pc.localDescription)
        elif obj is BYE:
            print("Exiting")
            break

if __name__ == "__main__":
    print("Initializing Client...")
    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    pc = RTCPeerConnection()
    recorder = MediaRecorder("video.mp4")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run_client(
                signaling,
                pc,
                recorder
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        # cleanup
        loop.run_until_complete(recorder.stop())
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())
