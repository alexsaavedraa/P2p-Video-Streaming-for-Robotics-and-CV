from aiortc.contrib.signaling import (TcpSocketSignaling, 
                                      BYE)
from aiortc import (RTCPeerConnection, 
                    RTCSessionDescription)
import asyncio

from video_player import VideoStreamPlayer, process_images
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
                print(result)
    print("Exiting process a")
               

async def run_client(signaling, pc, player):
    @pc.on("track")
    def on_track(track):
        print("Receiving %s" % track.kind)
        player.addTrack(track)

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
