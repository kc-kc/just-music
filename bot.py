import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import random
import os

admin_list = ['kc#0123']

TOKEN = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix = '_')

ytdlopts = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = YoutubeDL(ytdlopts)


@bot.command()
async def hello(ctx):
    await ctx.send('Hello there')


@bot.command()
async def rng(ctx, max: int):
    await ctx.send(random.randint(1, max))


@bot.command()
async def rename(ctx, name):
    if str(ctx.message.author) in admin_list:
        await bot.user.edit(username=name)
    else:
        await ctx.send('ur not allowed to do that...')


@bot.command()
async def play(ctx, url):
    await summon(ctx)

    voice_client = ctx.voice_client

    data = ytdl.extract_info(url, download=False)
    stream_url = data['formats'][0]['url']

    audio = discord.FFmpegPCMAudio(stream_url)
    voice_client.play(audio)


@bot.command()
async def pause(ctx):
    voice_client = ctx.voice_client
    if not voice_client.is_paused():
        voice_client.pause()


@bot.command()
async def resume(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_paused():
        voice_client.resume()


@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    voice_client.stop()


@bot.command()
async def summon(ctx):
    voice_client = ctx.voice_client  # Attempts to join voice channel if not already in one
    if not voice_client:
        voice_client = await ctx.author.voice.channel.connect()


@rename.error
async def rename_error(ctx, error):
    print(error)
    await ctx.send('```{}```'.format(error))


bot.run(TOKEN)

