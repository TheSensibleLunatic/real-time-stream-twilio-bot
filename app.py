from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Start, Stream
import os

app = Flask(__name__)

# Route to handle incoming voice calls from Twilio
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    if request.method == 'GET':
        return "Twilio voice endpoint is live.", 200

    response = VoiceResponse()

    # Start streaming the audio to the WebSocket server
    start = Start()
    start.stream(url="wss://your-cloudflare-tunnel-id.trycloudflare.com/stream")  # Replace with your actual WebSocket server URL
    response.append(start)

    # Speak something to the user
    response.say("You may begin speaking. This call is streaming audio in real time.")
    return Response(str(response), mimetype='text/xml')

if __name__ == "__main__":
    os.makedirs("recordings", exist_ok=True)  # Ensure recordings folder exists
    app.run(host="0.0.0.0", port=5000, debug=True)
