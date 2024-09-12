from ast import Lambda
from pickle import FALSE
from def_funtion import search_songUrl
from def_funtion import youtube
#from calendar import c
#from http import client
from queue import Empty
from re import search
from turtle import title
from types import LambdaType
from typing import Container
#from wsgiref import headers
from yt_dlp import YoutubeDL
#from youtube_dl import YoutubeDL
import discord
from discord.ext import tasks, commands
#import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from discord import FFmpegPCMAudio
import urllib.request,urllib.error
#import requests
import os,shutil
import time
import json
#import pandas as pd
#import matplotlib.pyplot as plt
#import asyncio
#import yt_dlp as youtube_dl
#from bs4 import BeautifulSoup;
#import concurrent.futures
#try:
#    youtube = build('youtube', 'v3', developerKey=API_key)
#except Exception as ex:
#    print(ex)
Bs4_headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
intents = discord.Intents.default()
client = discord.Client(intents=intents)
with open('setting.json','r',encoding='utf-8') as jfile:
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


@bot.command()
async def d(ctx, arg, arg2):
    header={
        'access-control-allow-origin': 'https://v.myself-bbs.com',
        'access-control-expose-headers' : ' X-Cache-Status',
        'content-encoding': 'gzip',
        'content-type': 'application/vnd.apple.mpegurl',
         'server': 'nginx',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        
      }
    pic2=discord.File(r"E:\picture\downloadok.jpg")
    url_m3u8=arg
    videoname=url_m3u8.split('/')[-2]
    path =os.path.join(r'E:\animation' , str(arg2))
    if not os.path.exists(path):
        os.makedirs(path)
    times=0
    urldata_m3u8 = urllib.request.urlopen(url_m3u8,timeout=20)
    num=0
    tempname_video=os.path.join(path,f'{num}.ts')
    for line in urldata_m3u8:
        url_ts=line.decode('utf-8')
        tempname_ts=os.path.join(path,f'{num}.ts')
        if not ".ts"in url_ts:
            continue
        else:
            if not url_ts.startswith("http"):
                url_ts=url_m3u8.replace(url_m3u8.split('/')[-1],url_ts)
        print(url_ts)
        urllib.request.urlretrieve(url_ts,filename=tempname_ts)
        if num == 0:
            shutil.move(tempname_ts,tempname_video)
            num += 1
            times+=1
            continue
        cmd=f'copy /b {tempname_video}+{tempname_ts} {tempname_video}'
        res=os.system(cmd)
        if res ==0:
            os.system(f'del {tempname_ts}')
            if times == 20:
                time.sleep(2)
                times=0
        print(f'Wrong,copy {num} .ts --> {videoname}.ts failure')
    os.system(f'del{path}/*.ts')
    filename=os.path.join(path,f'{videoname}.mp4')
    shutil.move(tempname_video,filename)
    print("finish")
    await ctx.send("finish")
    await ctx.send(file= pic2)

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

def next(ctx,url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False','extractor_retries': 'auto'}
    FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'}
    if len(urls) != 0:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        url = urls[0]
        del urls[0]
        with YoutubeDL(YDL_OPTIONS) as ydl:
              info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after = lambda x: next(ctx,url))


def search_songUrl(u):
    result =youtube.search().list(q=u,part='snippet',type='video',maxResults=10)
    re=result.execute()
    reTitle=re['items'][0]['snippet']['title']
    reUrl=re['items'][0]['id']['videoId']
    return reUrl,reTitle

@bot.command()
async def play( ctx,*,SongName:str=""):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        YDL_OPTIONS = {"format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0"}
        FFMPEG_OPTIONS = {
           'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
           'options': '-vn',}
        bot.volume=0.6
        SongId=search_songUrl(SongName)[0]
        SongTitle=search_songUrl(SongName)[1]
        url='https://www.youtube.com/watch?v='+SongId
        print(url)

        urls.append(url)
        #await ctx.send("now palying {} {}".format(SongTitle,url))
        if not voice.is_playing():
                
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                URL = info['url']

                voice.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS),after=lambda x :next(ctx,url))
                voice.is_playing()
                #await ctx.send('Bot is playing')
                await ctx.send("now palying {} {}".format(SongTitle,url))
                if len(urls)!=0:
                    urls.pop(0)
        

        else:
                await ctx.send(f"add song list {SongTitle} {url}")
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
