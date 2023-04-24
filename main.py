import asyncio
from pyrogram import Client
from pyrogram.types import Message
from tqdm import tqdm
import instaloader
import os

L = instaloader.Instaloader()

API_ID = 9967216
API_HASH = "fdee592a12f5c7cf74ab7c9023bcf160"
BOT_TOKEN = "6226275737:AAF6WdqcJ2F8hDyJyfq2LcIz87Ml-gqKPVg"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def download_reel(url):
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        with tqdm(total=1, desc="Downloading reel", unit="reel") as pbar:
            L.download_reels([post], os.path.join(os.getcwd(), "videos"), postprocessor=None, on_download=lambda: pbar.update(1))
        print("Reel downloaded successfully!")
    except Exception as e:
        print(f"Failed to download reel: {e}")

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

@app.on_message()
async def handle_message(client, message):
    await app.send_message(message.chat.id, "Hello, World!")
    download_reel(message.text)
    #await app.send_video(message.chat.id, "video.mp4", progress=progress, caption="video caption")

app.run()
