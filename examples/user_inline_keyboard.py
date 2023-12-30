import asyncio

from pyromod import Client, ikb
from pyrogram import filters, idle

api_id = 123456
api_hash = "your_api_hash"
bot_token = "your_bot_token"

user = Client("my_account", api_id, api_hash)
bot = Client("my_bot", api_id, api_hash)


@bot.on_callback_query(filters.regex("hello"))
async def handler(client, callback_query):
    await callback_query.answer("You clicked me! Hello!", show_alert=True)


@bot.on_callback_query(filters.regex("ping"))
async def handler(client, callback_query):
    await callback_query.answer("Pong!")


async def main():
    await user.start()
    await bot.start()

    await user.setup_inline_bot(bot)

    keyboard = ikb([
        [("pyromod", "github.com/pyromod", "url"), ("pyromod chat", "t.me/pyromodchat", "url")],
        [("Hello!", "hello"), ("Ping", "ping")],
    ])

    await user.send_message("me", "Hello world!", reply_markup=keyboard)
    print("Message sent! Check your saved messages!")

    await idle()

    await user.stop()
    await bot.stop()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())