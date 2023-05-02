import os
import requests
import time
import logging
from telethon import TelegramClient, events
from flask import Flask

# Replace with your own Telegram API credentials
api_id = 3477714
api_hash = '1264d2d7d397c4635147ee25ab5808d1'
bot_token = '6280315266:AAESKGYVWVlfcKW5XYQobzW_l50wbe73zyM'

# Initialize the Telegram bot
bot = TelegramClient('bot', api_id, api_hash)

# Initialize Flask web server
app = Flask(__name__)

@app.route("/")
def index():
    return f"Bot is running. Uptime: {int(time.time() - start_time)} seconds."

# Define the message handler for when the bot receives a file
@bot.on(events.NewMessage(func=lambda e: e.document or e.photo or e.video or e.audio or e.voice))
async def handle_file(event):
    # Send a message to the user
    await event.respond('Downloading file...')
    # Download the file using the Telegram API
    file = await event.download_media()
    # Send a message to the user
    await event.respond('File downloaded. Uploading to Transfer.sh...')
    # Upload the file to Transfer.sh using the API
    url = 'https://transfer.sh/'
    with open(file, 'rb') as f:
        response = requests.put(url + os.path.basename(file), data=f)
    # Send a message to the user with the link
    if response.status_code == 200:
        link = response.content.decode('utf-8')
        await event.respond(f'File uploaded successfully. Link: {link}')
    else:
        await event.respond('Failed to upload file.')
    # Delete the file from our server
    os.remove(file)

# Define the command handlers
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hi! Send me a file to download and upload to Transfer.sh.')

@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond('Available commands:\n'
                         '/start - Start the bot\n'
                         '/help - Display this help message')

async def main():
    # Start the bot
    await bot.start(bot_token=bot_token)
    print('Bot started.')
    # Start the Flask web server
    app.run(host='0.0.0.0', port=8080)
    await bot.run_until_disconnected()

if __name__ == '__main__':
    # Store the start time of the script
    start_time = time.time()
    # Run the main function
    import asyncio
    asyncio.run(main())
