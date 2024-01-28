from aiortc.contrib.signaling import (TcpSocketSignaling, 
                                      BYE)
from aiortc import (RTCPeerConnection, 
                    RTCSessionDescription)
import asyncio
import cv2
import numpy as np
import time

from video_player import VideoStreamPlayer
import multiprocessing

HOST = "127.0.0.1"
PORT = 1234

def process_frame_array(image_queue, termination_event):
    print("Initializing Image Recognition Thread")
    while not termination_event.is_set():
        image = image_queue.get()
        if image is not None:
            result = process_images(image)
            if result is not None:
                pass
                #print(result)
    print("Exiting process a")

def process_images(frame_array):
    gray = cv2.cvtColor(frame_array, cv2.COLOR_BGR2GRAY) 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 10, 
                param2 = 30, minRadius = 15, maxRadius = 25) 
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles)) 
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            cv2.circle(frame_array, (a, b), r, (0, 255, 0), 2) 
            cv2.circle(frame_array, (a, b), 1, (0, 0, 255), 3) 
            cv2.waitKey(10) 
            cv2.imshow("Detected Circle", frame_array)
            return a,b,r

async def run_client(signaling, pc, player):
    @pc.on("track")
    def on_track(track):
        print("Receiving %s" % track.kind)
        player.addTrack(track)

    channel = pc.createDataChannel("chat")
    print("channel created by local")

    async def send_circle_coordinates():
        while True:
            channel.send(str(time.time()))
            await asyncio.sleep(1)
    @channel.on("open")
    def on_open():
        asyncio.ensure_future(send_circle_coordinates())

    while True:
        obj = await signaling.receive()
        if isinstance(obj, RTCSessionDescription):
                await pc.setRemoteDescription(obj)
                await player.start()
                if obj.type == "offer":
                    await pc.setLocalDescription(await pc.createAnswer())
                    await signaling.send(pc.localDescription)
        elif obj is BYE:
            print("Exiting")
            break

        

if __name__ == "__main__":
    print("Initializing Client...")   
    #Multiprocess setup here
    image_queue = multiprocessing.Queue()
    termination_event = multiprocessing.Event()
    process_a = multiprocessing.Process(target=process_frame_array, args=(image_queue,termination_event))
    process_a.start()

    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    pc = RTCPeerConnection()
    player = VideoStreamPlayer("Nimble Challenge", image_queue)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run_client(
                signaling,
                pc,
                player
            )
        )
    except KeyboardInterrupt:
        pass
    finally:

        #Close all processes
        termination_event.set()
        process_a.join()
        loop.run_until_complete(player.stop())
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())
