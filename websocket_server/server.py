import asyncio
import websockets
import base64
import json
import os
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

AUDIO_DIR = "audio_output"
os.makedirs(AUDIO_DIR, exist_ok=True)

chunk_counter = 0
buffer_audio = bytearray()
silence_threshold = -40  # dBFS
silence_padding = 1000  # ms

def save_audio(data_bytes):
    global chunk_counter

    audio = AudioSegment(data_bytes, sample_width=2, frame_rate=8000, channels=1)
    nonsilent = detect_nonsilent(audio, min_silence_len=500, silence_thresh=silence_threshold)

    if nonsilent:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{AUDIO_DIR}/chunk_{now}_{chunk_counter}.wav"
        audio.export(filename, format="wav")
        print(f"[SAVED] Audio chunk with speech: {filename}")
        chunk_counter += 1
    else:
        print("[SKIPPED] Only silence detected.")


async def handle_stream(websocket):
    global buffer_audio

    print("[CONNECTED] WebSocket client connected")

    try:
        async for message in websocket:
            msg = json.loads(message)
            if msg.get("event") == "media":
                media = msg["media"]
                payload = base64.b64decode(media["payload"])
                buffer_audio.extend(payload)

                # Optional: Process every ~5 seconds or after enough data
                if len(buffer_audio) > 8000 * 2 * 5:  # 5 seconds of audio
                    save_audio(bytes(buffer_audio))
                    buffer_audio = bytearray()

            elif msg.get("event") == "stop":
                print("[STOP] Stream ended.")
                if buffer_audio:
                    save_audio(bytes(buffer_audio))
                    buffer_audio = bytearray()

    except websockets.exceptions.ConnectionClosed:
        print("[DISCONNECTED] WebSocket connection closed.")


async def main():
    print("[STARTING] WebSocket server on ws://0.0.0.0:8765")
    async with websockets.serve(handle_stream, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
