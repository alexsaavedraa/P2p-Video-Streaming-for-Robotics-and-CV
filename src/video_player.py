import cv2
import asyncio
from aiortc.contrib.media import (MediaStreamTrack,
                                  MediaStreamError)

class VideoStreamPlayer():
    def __init__(self, title:str, image_queue,x):
        self.title = title
        self.image_queue = image_queue
   
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
            
            try:
                frame = await self.track.recv()
            except MediaStreamError: 
                return
            frame_array = frame.to_rgb().to_ndarray()
            i+=1
            self.image_queue.put(frame_array)