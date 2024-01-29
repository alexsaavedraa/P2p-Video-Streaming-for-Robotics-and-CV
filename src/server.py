from aiortc.contrib.signaling import (TcpSocketSignaling, 
                                      BYE)
from aiortc import (RTCPeerConnection, 
                    RTCSessionDescription,
                    RTCDataChannel)
import asyncio
from bounce_ball import BounceBallStreamTrack
import numpy as np
import cv2

HOST = "127.0.0.1"
PORT = 1234


def euclid_distance(coords1: list, coords2: list) -> float:
    '''Calculates the euclidean distance between two points'''
    sqr = (coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2
    return sqr**.5

def display_error(coords_act: list, coords_pred: list, error: float) -> None:
    "Displays the difference between the actual and detected location of two balls"
    frameHeight = 640
    frameWidth = 480
    real_color = (0,254,0)
    recognized_color = (0,0,254)
    img = np.zeros((frameHeight, frameWidth, 3),
                        dtype='uint8') 
    cv2.circle(img,
                   coords_act,
                   20,
                   real_color,
                   -1)
    cv2.circle(img,
                   coords_pred,
                   20,
                   recognized_color,
                   thickness=2)
    
    
    img = cv2.putText(img, f'Error: {str(round(error,1)+0.0)}px',(30,30), cv2.FONT_HERSHEY_SIMPLEX , 1 ,(254,254,254), 2, cv2.LINE_AA) 
    cv2.imshow("Server: Error Detection", img)
    cv2.waitKey(1)
    

def process_message(message: str, track:BounceBallStreamTrack) -> None:
    '''Takes in message and the the ball bounce object. Aligns the 
    generated video frame with the client detected coordinates frame'''
    message = message.split(',')
    message = [int(x) for x in message]
    try:
        errors = euclid_distance(track.frame_dict[message[0]-2], [message[1], message[2]] )
        display_error(track.frame_dict[message[0]-2], [message[1], message[2]], errors)
    except:
        pass


async def run_server(signaling: TcpSocketSignaling, pc: RTCPeerConnection, track: BounceBallStreamTrack, channel:RTCDataChannel ):
    '''Consumes all signalling: connects, creates offer, then consumes the signaling. Handles datastream messages'''
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