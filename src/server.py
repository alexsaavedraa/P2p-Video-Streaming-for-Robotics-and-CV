from aiortc.contrib.signaling import (TcpSocketSignaling, 
                                      BYE)
from aiortc import (RTCPeerConnection, 
                    RTCSessionDescription)
import asyncio
from bounce_ball import BounceBallStreamTrack
import numpy as np
import cv2

HOST = "127.0.0.1"
PORT = 1234


def euclid_distance(coords1, coords2):
    sqr = (coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2
    return sqr**.5

def display_error(coords1, coords2, error):
    frameHeight = 640
    frameWidth = 480
    real_color = (0,254,0)
    recognized_color = (0,0,254)
    img = np.zeros((frameHeight, frameWidth, 3),
                        dtype='uint8') 
    cv2.circle(img,
                   coords1,
                   20,
                   real_color,
                   -1)
    cv2.circle(img,
                   coords2,
                   20,
                   recognized_color,
                   thickness=2)
    
    
    
    cv2.imshow("Server: Error Detection", img)
    cv2.waitKey(1)
    

def process_message(message, track):
    message = message.split(',')
    message = [int(x) for x in message]
    try:
        #print("Processing Message:", message, track.frames[-1], track.frame_dict[message[0]-3])
        errors = euclid_distance(track.frame_dict[message[0]-2], [message[1], message[2]] )
        display_error(track.frame_dict[message[0]-2], [message[1], message[2]], errors)
        print(errors)



    except:
        pass
        #print('not enough frames yet')

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
                track,
                channel
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())