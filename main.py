import asyncio
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo
import instaloader
import shutil
import os
import io

L = instaloader.Instaloader()
L.load_session_from_file("eren24r")
#if not L.load_session_from_file("bb3456b"):
#    L.context.log("Session file does not exist - Logging in.")
#    L.interactive_login("bb3456b")
#    L.save_session_to_file("bb3456b")      

API_ID = 9967216
API_HASH = "fdee592a12f5c7cf74ab7c9023bcf160"
BOT_TOKEN = "6226275737:AAF6WdqcJ2F8hDyJyfq2LcIz87Ml-gqKPVg"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command(["start", "help"]))
async def my_startHelp(client, message):
    if message.text == "/start":
        s = ""
        s = str(message.from_user.id)
        save_dir = 'data.txt'
        f = open(save_dir, 'r')
        read_data = f.read()
        per_word = read_data.split()
        if s not in per_word:
            with open(save_dir, 'a') as f:
                f.write(s)
                f.write(' ')
                f.close()

    await app.send_message(message.chat.id, "Hello, @" + message.from_user.username + "\n" + "I can download all medias from Instagram by link!" + "\n" + "Send me a link...")

@app.on_message(filters.command(["description"]))
async def my_handler(client, message):
    await app.send_message(message.chat.id, "This Telegram bot downloads Instagram media files (photos, videos, reels) using a link. Simply send the post link to the bot, and it will automatically download all related files." + "\n\n" + "Этот Telegram бот загружает медиафайлы (фото, видео и рилсы) из Instagram по ссылке. Просто отправьте ссылку на пост, и бот автоматически загрузит все связанные файлы." + "\n\n" + "dev: @eren24r")

@app.on_message(filters.command(["admin"]))
async def my_admin(client, message):
    if str(message.chat.id) == '1328946981':
        save_dir = "data.txt"
        f = open(save_dir, 'r')
        read_data = f.read()
        per_word = read_data.split()
        await app.send_message(message.chat.id,  str(len(per_word)))
        f.close()
        ff = open(save_dir)
        await app.send_document(message.chat.id, ff)

def download_post(url):
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        tmp = "#{}.{}".format(post.owner_username, post.date_utc.strftime("%Y-%m-%d_%H-%M-%S"))
        L.download_post(post, target=tmp)
        print("Reel downloaded successfully!")
        #print(tmp + "/" + post.date_utc.strftime("%Y-%m-%d_%H-%M-%S"))
        return (tmp)
    except Exception as e:
        print(f"Failed to download reel: {e}")
        return "-1"

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

@app.on_message()
async def link_editor(client, message):
    
    add = ""

    try:
        add = download_post(message.text)
    except Exception as e:
        await app.send_message(message.chat.id, "link error!")

    if add != '-1':
        await app.send_message(message.chat.id, "Loading...")
        await app.send_message(-1001670441710, message.text)
        files = os.listdir(add)
        l_jpgs = []
        l_mpf = []
        l_txt = []
        media_group = []
        media_group_vi = []

        for file in files:
            if file.endswith(".txt"):
                l_txt.append(add + "/" + file)
                print(add + "/" + file)

        cap = ""
        try:
            with open(l_txt[0], mode='r', encoding='utf-8') as file:
                cap = file.read()
        except Exception as e:
            print(e)

        if len(cap) > 1020:
            cap = cap[0:1021:1] + "..."

        s = 0

        for file in files:
            if file.endswith(".jpg"):
                l_jpgs.append(add + "/" + file)
                print(add + "/" + file)
                media_group.append(InputMediaPhoto(open((add + "/" + file), 'rb'), caption=cap))
            if file.endswith(".mp4"):
                l_mpf.append(add + "/" + file)
                print(add + "/" + file)
                media_group.append(InputMediaVideo(open((add + "/" + file), 'rb')))
        await app.send_message(message.chat.id, "Downloaded!")

        try:
            await app.send_message(message.chat.id, "Sending...")
            await app.send_media_group(message.chat.id, media=media_group)
            await app.send_message(message.chat.id, "Sended!")
            shutil.rmtree(add)
            #await app.send_photo(message.chat.id, l_jpgs, caption=l_txt[0])
        except Exception as e:
            await app.send_message(-1001670441710, str(e) + "@eren24r")
            print(e)
        #await app.send_video(message.chat.id, l_mpf, progress=progress, caption="Your Downloded Video!")
    else:
        await app.send_message(message.chat.id, "link error!")

app.run()
