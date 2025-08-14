import os
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from dotenv import load_dotenv

# Load env file locally (Render me env vars panel se set hote hain)
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
SOURCE = os.getenv("SOURCE")  # Source chat username/id
DESTINATION = os.getenv("DESTINATION")  # Destination chat username/id

# Flask app for keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Userbot is running!"

# Telethon client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE))
async def handler(event):
    try:
        await client.send_message(DESTINATION, event.message)
        print(f"Forwarded message: {event.message.text}")
    except Exception as e:
        print(f"Error forwarding: {e}")

def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    client.start()
    me = client.loop.run_until_complete(client.get_me())
    print(f"Logged in as: {me.first_name} (@{me.username})")
    print("Listening for new messages...")
    client.run_until_disconnected()
