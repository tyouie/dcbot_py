#from ast import Lambda
from def_funtion import search_songUrl
from def_funtion import youtube
#from calendar import c
#from http import client
from queue import Empty
#from re import search
#from turtle import title
from types import LambdaType
from typing import Container
#from wsgiref import headers
#from youtube_dl import YoutubeDL
import discord
import ffmpeg
from discord.ext import tasks, commands
#import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from discord import FFmpegPCMAudio
#import urllib.request,urllib.error
#import requests
#import os,shutil
#import time
import json
#import pandas as pd
#import matplotlib.pyplot as plt
#import asyncio
from yt_dlp import YoutubeDL
#from bs4 import BeautifulSoup;
#import concurrent.futures
import asyncio
intents = discord.Intents.default()
client = discord.Client(intents=intents)
with open('setting.json', 'r',encoding='utf-8') as jfile:
    jdata=json.load(jfile)
bot=commands.Bot(command_prefix='!',intents=intents)
intents.message_content = True

@bot.event
async def on_ready():
    print('online')

@bot.event
async def on_member_join(member):
    channel=bot.get_channel(int(jdata["channel"]))
    await channel.send(f'{member} welcome')

@bot.event
async def on_member_remove(member):
    channel=bot.get_channel(int(jdata["channel"]))
    await channel.send(f'{member} leave')
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} (ms)')



@bot.command(pass_context=True)
async def join(ctx):
    voice_channel=ctx.author.voice.channel
    #voice = get(bot.voice_client,guild=ctx.guild)

    await voice_channel.connect()
    await ctx.send(f"join {ctx.author.voice.channel} voice channel")
urls=[]
@bot.command()
async def quit(ctx):
        voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
        global urls
        urls=[]
        await voice.disconnect()

async def next(ctx):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False','retries': 5}
    FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'}
    if len(urls) == 0:
         await ctx.send("list doesn't have any song")
         return
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    url = urls.pop(0)
    def get_audio_info():
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    #info = ydl.extract_info(url, download=False)
                    return ydl.extract_info(url, download=False)
    info = await asyncio.to_thread(get_audio_info)
    URL = info['url']
    def after_playing(error):
        # 使用 asyncio.run_coroutine_threadsafe 呼叫 async 函式
        fut = asyncio.run_coroutine_threadsafe(next(ctx), bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"Error in after callback: {e}")
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=after_playing)
    await ctx.send(f"now playing {info.get('title','Unknown Title')}")


def search_songUrl(u):
    result =youtube.search().list(q=u,part='snippet',type='video',maxResults=10)
    re=result.execute()
    reTitle=re['items'][0]['snippet']['title']
    reUrl=re['items'][0]['id']['videoId']
    return reUrl,reTitle

@bot.command()
async def play( ctx,*,SongName:str=""):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False','retries': 5}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'}
        bot.volume=0.6
        SongId,SongTitle=search_songUrl(SongName)
        url='https://www.youtube.com/watch?v='+SongId
        urls.append(url)
        #await ctx.send("now palying {} {}".format(SongTitle,url))
        if not voice.is_playing():
                """def get_audio_info():
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        #info = ydl.extract_info(url, download=False)
                        return ydl.extract_info(url, download=False)
                info = await asyncio.to_thread(get_audio_info)
                URL = info['url']
                def after_playing(error):
                    if error:
                        print(f"Playback error: {error}")
                    if len(urls) > 0:
                        fut = asyncio.run_coroutine_threadsafe(next(ctx), bot.loop)
                        try:
                            fut.result()
                        except Exception as e:
                            print(f"Error in after callback: {e}")
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=after_playing)
                voice.is_playing()
                #await ctx.send('Bot is playing')
                urls.pop(0)"""
                await next(ctx)
        

        else:
                return


@bot.command()
async def volume(ctx):
    await ctx.send(bot.volume*10)
@bot.command()
async def volumeup(ctx,value:int):
    bot.volume += (value/10)
    await ctx.send(bot.volume*10)
    
@bot.command()
async def volumedown(ctx,value:int):
    bot.volume -= (value/10)
    await ctx.send(bot.volume*10)
@bot.command()
async def skip(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
def list_yt_api(Title,urls):
    for i in range(len(urls)):
        url=urls[i]
        url=url[url.find('=')+1:]
        request=youtube.videos().list(part="snippet",id=url)
        respond=request.execute()
        Title.append(respond['items'][0]['snippet']['title'])

@bot.command()
async def list(ctx):
    Title=[]
    list_yt_api(Title,urls)
    embed=discord.Embed(title="song title")
    embed.set_thumbnail(url="https://truth.bahamut.com.tw/s01/202310/523bf14774ca0900a5d639811d6acfaa.PNG")
    for i in range(len(Title)):
        embed.add_field(name=i+1, value=Title[i], inline=False)
    await ctx.send(embed=embed)
   
    #await ctx.send(Title)
    #print(Title)



bot.run(jdata['token'])
