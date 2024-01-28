import cv2
import numpy as np
from aiortc import (VideoStreamTrack)
from av import VideoFrame

class Ball():
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.frames = []
        self.frame_dict = {}

    def increment_position(self, dx, dy):
        self.x += dx
        self.y += dy
            
        
class BounceBallStreamTrack(VideoStreamTrack):
    """
    A video track that returns an animated flag.
    """

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.frames = []
        self.frame_dict = {}
        self.frameWidth = 480
        self.frameHeight = 640
        self.ball = Ball(x=100, 
                         y=100, 
                         r=20, 
                         color=(255,0,0))
        self.dx = 5
        self.dy = -5
        
    def get_next_frame(self):    
        img = np.zeros((self.frameHeight, self.frameWidth, 3),
                        dtype='uint8') 
        
        cv2.circle(img,
                   (self.ball.x, self.ball.y),
                   self.ball.r,
                   self.ball.color,
                   -1)

        self.ball.increment_position(self.dx, self.dy)

        if self.ball.y >=self.frameHeight-self.ball.r:
            self.dy *= -1
        elif self.ball.y<=self.ball.r:
            self.dy *= -1
        if self.ball.x >=self.frameWidth-self.ball.r:
            self.dx *= -1
        elif self.ball.x<=self.ball.r:
            self.dx *= -1
        
        res = VideoFrame.from_ndarray(img, format="rgb24")
        return res


    async def recv(self):
        pts, time_base = await self.next_timestamp()
        frame = self.get_next_frame()
        self.frames.append([self.counter, self.ball.x, self.ball.y])
        self.frame_dict[self.counter] = [self.ball.x, self.ball.y]

        frame.pts = pts
        frame.time_base = time_base
        self.counter += 1
        return frame


    
