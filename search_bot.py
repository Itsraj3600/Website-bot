# search_bot.py
from pyrogram import Client, filters
from pyrogram.types import Message
import os

API_ID = int(os.getenv("API_ID"))          # Get this from https://my.telegram.org
API_HASH = os.getenv("API_HASH")            # Get this from https://my.telegram.org
BOT_TOKEN = os.getenv("BOT_TOKEN")          # Your BotFather token
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))   # Your channel id (e.g., -100xxxxxxxxxx)

app = Client("movie_search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("search") & filters.private)
async def search_movie(client: Client, message: Message):
    query = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if not query:
        return await message.reply("❗ Please provide a search term.")

    results = []

    async for msg in app.search_messages(CHANNEL_ID, query):
        if msg.video or msg.document:
            results.append(f"🎬 {msg.caption or 'No Title'}\n/file_{msg.id}")
        if len(results) >= 5:
            break

    if not results:
        await message.reply("❌ No movies found.")
    else:
        await message.reply("\n\n".join(results))

@app.on_message(filters.command("file") & filters.private)
async def get_file_id(client: Client, message: Message):
    try:
        target_msg = await app.get_messages(CHANNEL_ID, int(message.text.split("_", 1)[1]))
        file_id = target_msg.document.file_id if target_msg.document else target_msg.video.file_id
        title = target_msg.caption or "Movie"
        await message.reply(f"✅ *{title}*\nFile ID: `{file_id}`", parse_mode="markdown")
    except:
        await message.reply("⚠️ Failed to fetch the file ID.")

if __name__ == "__main__":
    app.run()