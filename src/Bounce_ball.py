import cv2
import numpy as np
from aiortc.contrib.signaling import (TcpSocketSignaling, 
                                      BYE)
from aiortc import (RTCPeerConnection, 
                    RTCSessionDescription,
                    VideoStreamTrack)
from av import VideoFrame
W,L = 480, 640 


            





class Bounce_ball(VideoStreamTrack):
    """
    A video track that returns an animated flag.
    """

    def __init__(self):
        super().__init__()  # don't forget this!
        self.counter = 0
        self.frames = []
        self.x = 100
        self.y = 100
        self.dx = 5
        self.dy = -5
        for i in range(30):
            self.frames.append(self.get_next_frame())

        
    def get_next_frame(self):
        img = np.zeros((W,L,3),dtype='uint8')
        
    
        img = np.zeros((L,W,3),dtype='uint8') 
        self.x = self.x+self.dx
        self.y = self.y+self.dy
        cv2.circle(img,(self.x,self.y),20,(255,0,0),-1)
        if self.y >=L:
            self.dy *= -1
        elif self.y<=0:
            self.dy *= -1
        if self.x >=W:
            self.dx *= -1
        elif self.x<=0:
            self.dx *= -1
        
        res = VideoFrame.from_ndarray(
                    img, format="bgr24")
        return res


    async def recv(self):
        
        pts, time_base = await self.next_timestamp()

        frame = self.get_next_frame()
        frame.pts = pts
        frame.time_base = time_base
        self.counter += 1
        return frame


    