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
        
        self.x = 100
        self.y = 100
        self.dx = 5
        self.dy = -5

        
    def get_next_frame(self):
        img = np.zeros((X,Y,3),dtype='uint8')
        
    
        # Display the image
        img = np.zeros((L,W,3),dtype='uint8') 
        # Increment the position
        self.x = self.x+self.dx
        self.y = self.y+self.dy
        cv2.circle(img,(self.x,self.y),20,(255,0,0),-1)
        # Change the sign of increment on collision with the boundary
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

        frame = self.frames[self.counter % 30]
        frame.pts = pts
        frame.time_base = time_base
        self.counter += 1
        print(self.counter)
        return frame


    