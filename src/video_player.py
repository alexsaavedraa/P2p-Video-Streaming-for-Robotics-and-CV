import cv2
import asyncio
from aiortc.contrib.media import (MediaStreamTrack,
                                  MediaStreamError)
import numpy as np

class VideoStreamPlayer():
    def __init__(self, title:str, image_queue,x):
        self.title = title
        self.image_queue = image_queue
        self.x = x

    def addTrack(self, track: MediaStreamTrack):
        self.track = track

    async def start(self):
        print("Starting stream")
        asyncio.ensure_future(self.__run_track())

    async def stop(self):
        print("Stopping stream")
        cv2.destroyAllWindows()

    async def __run_track(self):
        frame = True
        i = 0
        while frame:
            print(self.x.value)
            try:
                frame = await self.track.recv()
            except MediaStreamError: 
                return
            frame_array = frame.to_rgb().to_ndarray()
            i+=1
            self.image_queue.put(frame_array)
            
            
            

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
            
            
    else:
        pass
        #print("Error, no circles detected")
