from aiortc.contrib.signaling import TcpSocketSignaling
from aiortc import RTCPeerConnection
import asyncio

HOST = "127.0. 0.1"
PORT = 8080

async def run_server(signaling, peer_connection, media, data_channel):
    await peer_connection.createOffer(media, data_channel)

if __name__ == "__main__":
    print("Initializing Server...")
    signaling = TcpSocketSignaling(host=HOST, port=PORT)
    peer_connection = RTCPeerConnection()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run_server(
            signaling, 
            peer_connection, 
            media,
            data_channel
        )
    )