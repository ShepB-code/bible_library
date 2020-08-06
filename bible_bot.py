#BIBLE BOT
import re
from collections import Counter

import discord
import itertools
from discord.ext import commands
import discord.utils

from bible_lib import Bible, BibleAPI

bot = commands.Bot(command_prefix='-')

with open("bible_api_key.txt", 'r') as f:
    bible = Bible(api_key=f.read().strip())
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('?info for commands'))
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')


@bot.listen('on_message')
async def my_message(message):
    channel = message.channel
    
    if message.author.id == bot.user.id:
        return
    
    books_in_message = (i for i in message.content.lower().split() if i in bible.get_books())

    if books_in_message:
        content = message.content.lower()
        for book in books_in_message:

            try:
                chapter, verse = content[content.index(book) + len(book):].split(" ", 2)[1].split(":", 1)

                verse_tuple = bible.get_verses(book_name=book, chapter=chapter, verse=verse)
                bible_verse = verse_tuple[0]

                for char in "[]":
                    bible_verse = bible_verse.replace(char, "**")
                verse_embed = discord.Embed(
                title=f'{book.capitalize()} {chapter}:{verse}',
                color=discord.Color.gold()
                )
                verse_embed.add_field(name="Verses:", value=bible_verse, inline=False)
                verse_embed.add_field(name='Want a Custom Bot?', value="[Discord Server](https://discord.gg/p7Gq4bH)", inline=False)

                verse_embed.set_footer(text='Made by Peter and Shep', icon_url=bot.user.avatar_url)
                content = content[content.index(book) + len(book):]

                await channel.send(embed=verse_embed)
            except Exception as err:
                print(err)

    

with open('bible_bot_token.txt', 'r') as f:
    bot.run(f.read().strip())
