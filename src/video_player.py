import cv2
import numpy
import asyncio
from aiortc.contrib.media import (MediaStreamTrack,
                                  MediaStreamError)
from av import VideoFrame

class VideoStreamPlayer():
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
                print("Received frame", i)
                i+=1
            except MediaStreamError:
                return
      
            cv2.waitKey(10)
            cv2.imshow('Frame', frame.to_rgb().to_ndarray()) 
        