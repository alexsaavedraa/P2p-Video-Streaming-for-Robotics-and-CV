import cv2
import numpy
import asyncio
from aiortc.contrib.media import (MediaStreamTrack,
                                  MediaStreamError)
from av import VideoFrame

class VideoStreamPlayer():
    def __init__(self, title:str):
        self.title = title

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
            cv2.imshow(self.title, frame_array) 
            cv2.waitKey(10)
            i+=1
        