from aiortc.contrib.signaling import (TcpSocketSignaling, 
                                      BYE)
from aiortc import (RTCPeerConnection, 
                    RTCSessionDescription)
import asyncio
from bounce_ball import BounceBallStreamTrack

HOST = "127.0.0.1"
PORT = 1234

def process_message(message, track):
    print("Processing Message:", message, track.frames[-1])

async def run_server(signaling, pc, track, channel):
    @channel.on("message")
    def on_message(message):
        process_message(message, track)

    await signaling.connect()
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)
    while True:
        obj = await signaling.receive()
        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)
        if obj is BYE:
            print("Exiting")
            break

if __name__ == "__main__":
    print("Initializing Server...")
    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    pc = RTCPeerConnection()

    track = BounceBallStreamTrack()
    pc.addTrack(track)

    channel = pc.createDataChannel("server")
    print(channel.label, "channel created locally")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run_server(
                signaling, 
                pc,
                channel,
                track

            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())