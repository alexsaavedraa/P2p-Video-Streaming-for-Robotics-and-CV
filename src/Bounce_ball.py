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
        res = []
        img = np.zeros((X,Y,3),dtype='uint8')
        dx,dy =5,5
        for i in range(600):
            # Display the image
            img = np.zeros((480,640,3),dtype='uint8') 
            # Increment the position
            x = x+dx
            y = y+dy
            cv2.circle(img,(x,y),20,(255,0,0),-1)
            # Change the sign of increment on collision with the boundary
            if self.y >=L:
                dy *= -1
            elif y<=0:
                dy *= -1
            if x >=W:
                dx *= -1
            elif x<=0:
                dx *= -1
            ##apend the frame
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


    