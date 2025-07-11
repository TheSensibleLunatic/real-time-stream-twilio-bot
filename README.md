﻿# twilio-real-time
# 🎧 Twilio Streaming Audio Receiver with Silence Detection

This project sets up a WebSocket server to receive streaming audio from Twilio Media Streams, detect speech using silence detection, and save individual audio files to disk.

---

## 🚀 Features

- Receives real-time audio from Twilio via WebSocket.
- Decodes audio (Base64, µ-law encoded, 8000 Hz, mono).
- Uses silence detection to split speech.
- Saves each spoken chunk as a `.wav` file in `audio_output/`.

---

## 📁 Project Structure

