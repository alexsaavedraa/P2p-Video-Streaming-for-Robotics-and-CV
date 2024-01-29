from aiortc.contrib.signaling import (TcpSocketSignaling, 
                                      BYE)
from aiortc.mediastreams import VIDEO_PTIME
from aiortc import (RTCPeerConnection, 
                    RTCSessionDescription)
import asyncio
import cv2
import numpy as np
from ctypes import c_int

from video_player import VideoStreamPlayer
import multiprocessing

HOST = "127.0.0.1"
PORT = 1234

def process_frame_array(image_queue:multiprocessing.Queue, 
                        termination_event:multiprocessing.Event,
                        x:int,
                        y:int,
                        frame_index:int):
    """Takes the next frame from the multiprocessing queue, runs a circle detection

    Args:
        image_queue (multiprocessing.Queue): source queue of images
        termination_event (multiprocessing.Event): event to stop processessing
        x (int): multiproceessing.Value to keep track of ball x coord
        y (int): multiproceessing.Value to keep track of ball y coord
        frame_index (int):multiproceessing.Value to keep track of curr frame index
    """    
    ''''''
    while not termination_event.is_set():
        image = image_queue.get()
        frame_index.value += 1
        if image is not None:
            result = process_image(image)
            if result is not None:
                x.value = result[0]
                y.value = result[1]
    print("Exiting process a")

def process_image(frame_array):
    '''Uses HoughCircles to find circles, returns x,y, and radius'''
    gray = cv2.cvtColor(frame_array, cv2.COLOR_BGR2GRAY) 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    detected_circles = cv2.HoughCircles(gray_blurred, 
                                        cv2.HOUGH_GRADIENT, 
                                        1, 
                                        20, 
                                        param1 = 10, 
                                        param2 = 30, 
                                        minRadius = 15, 
                                        maxRadius = 25) 
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles)) 
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            return a,b,r

async def run_client(signaling, pc, player):
    @pc.on("track") # pragma: no cover
    def on_track(track):
        print("Receiving %s" % track.kind)
        player.addTrack(track)

    @pc.on("datachannel") # pragma: no cover
    def on_datachannel(channel):
        print(channel.label, "channel created")
        asyncio.ensure_future(send_circle_coordinates(channel))

    async def send_circle_coordinates(channel): # pragma: no cover
        while True:
            data = f"{frame_index.value},{x.value},{y.value}"
            channel.send(data)
            await asyncio.sleep(VIDEO_PTIME)
    
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

        
if __name__ == "__main__": # pragma: no cover
    print("Initializing Client...")   
    #Multiprocess setup here
    image_queue = multiprocessing.Queue()
    termination_event = multiprocessing.Event()

    x = multiprocessing.Value(c_int, 0)
    y = multiprocessing.Value(c_int, 0)
    frame_index = multiprocessing.Value(c_int, 0)

    process_a = multiprocessing.Process(target=process_frame_array, args=(image_queue,termination_event, x,y,frame_index))
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
