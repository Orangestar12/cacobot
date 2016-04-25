import re
import json
import os

from random import choice

import discord
from apiclient.discovery import build # pylint: disable=e0401

import cacobot.base as base

mention_syntax = re.compile(r'(<@([0-9#]*?)>)')

youtube = build(base.config['youtube']['API_SERVICE_NAME'], base.config['youtube']['API_VERSION'], developerKey=base.config['youtube']['DEVELOPER_KEY'])

@base.cacofunc
async def yt(message, client):
    '''
    **{0}yt** <*query*> [.results *int*]
    Searches YouTube and returns the first query. If you provide `.results` with an integer afterwards, returns the first *int* results.
    *Example: `{0}yt Doom E1M1 100% .results 3`*
    '''

    if message.content.split()[-2] == '.results':
        query = message.content[4:message.content.find('.results') - 2]
        results = int(message.content.split()[-1]) #The number of results to spew.
    else:
        query = message.content[4:]
        results = 1

    #This string will store the message that will eventually be sent.
    all_videos = ''

    #Limit requests if exceeds base.config
    if results > base.config['youtube']['request_limit']:
        all_videos += '*I had to limit your request to {} results at the behest of my maintainer.*\n'.format(base.config['youtube']['request_limit'])
        results = base.config['youtube']['request_limit']

    #this is all pretty much from the YouTube API Python example.

    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=results,
        type='video'
        ).execute()

    vids = []

    for search_result in search_response.get('items', []):
        vids.append('**' + search_result['snippet']['title'] + '** | http://youtu.be/' + search_result['id']['videoId'])

    for video in range(0, len(vids)):
        all_videos += vids[video] + ' (Result ' + str(video + 1) + ' of ' + str(len(vids)) + ' from YouTube) \n\n'

    await client.send_message(message.channel, all_videos)

# Load musicbot list
try:
    with open('configs/musicbots.json') as Z:
        musicbots = json.load(Z)
# Create tags if not found
except FileNotFoundError:
    with open('configs/musicbots.json', 'w') as Z:
        Z.write('{}')
        musicbots = {}

doommuse = [
    'https://youtu.be/AjEx292Ph8M',
    'https://youtu.be/104GjEBZt1k',
    'https://youtu.be/SzI7DLR0DPU',
    'https://youtu.be/VghIvkUd_nY'
]

doomsnark = [
    'THE SOUNDTRACK TO MY NIGHTMARES',
    'HISSING INTENSIFIES',
    'AND THEN WE WERE ALL SHOT TO DEATH',
    'YOU GOT THE SHOTGUN',
    'PICKED UP A CLIP',
    'PICK ED UP A CLIP',
    'CHAINSAW! THE GREAT COMMUNICATOR!',
    '"BERSERK" IS A FUNNY WORD'
]

@base.cacofunc
async def ytadd(message, client):
    '''
    **{0}ytadd** [ *query* | *setup* <@mention invoker>]
    Searches YouTube for *query*, returns the first result, then clarifies with you before adding it to the queue for your music bot. If you deny the result, returns the next result and tries again. This goes until 5 results have been displayed, or the bot recieves `abort`.
    You can set the music bot for this server with this syntax: `{0}ytadd {0}setup @MusicBot botinvoker`, where @MusicBot is the mention for the bot account, and `botinvoker` is the bot's invoker character or string.
    *Example: `{0}ytadd I Sawed The Demons`, `{0}ytadd {0}setup @Musical Statue &play`*
    '''

    params = message.content.split()

    if len(params) == 1:
        await client.send_message(message.channel, '🚫 {}: You must provide either a YouTube search query or a setup string for your bot. Use `{}help ytadd` for more information.'.format(message.author.name, base.config['invoker']))
        return

    # set up music bot
    if params[1].lower() == '{}setup'.format(base.config['invoker']):
        if not message.channel.permissions_for(message.author).manage_server:
            await client.send_message(message.channel, '🚫 {0}: You must have the permission to manage the server to set or update the music bot for this server.'.format(message.author.name))
            return

        if len(params) < 4:
            await client.send_message(message.channel, '🚫 {}: The setup for a music bot must contain exactly two additional parameters: the mention representing the music bot in question, and the invoker for that music bot.'.format(message.author.name))
            return

        if not message.mentions:
            await client.send_message(message.channel, '🚫 {}: You must *mention* the bot you are trying to set up. (i.e. put an @ symbol before it.)'.format(message.author.name))
            return

        if not mention_syntax.match(params[2]):
            await client.send_message(message.channel, '🚫 {0}: Please make sure the bot mention in your command is the third parameter. (i.e. `{1}ytadd {1}setup @musicbot ;play`)'.format(message.author.name, base.config['invoker']))
            return

        msgbot = message.mentions[0].id
        msginvoker = message.content.split(None, 3)[3]
        msgserver = message.server.id

        musicbots[msgserver] = {
            'invoker' : msginvoker,
            'bot_id' : msgbot
        }

        with open('configs/musicbots.json', 'w') as z:
            json.dump(musicbots, z, indent=4)

        await client.send_message(message.channel, '✔ {}: I have successfully set/updated your server\'s music bot to {}. I will add videos to them with the syntax `{} {}`'.format(message.author.name, message.mentions[0].name, msginvoker, choice(doommuse)))
        return
    # end bot setup

    if base.stream:
        await client.send_message(message.channel, '🚫 {}: Sorry, I\'m currently playing music in another channel. (Someday discord.py will let me connect to multiple channels!!)'.format(message.author.name))
        return


    if message.server.id not in musicbots:
        await client.send_message(message.channel, '🚫 {}: There is no musicbot set for this server. Please have a server administrator set one up. Use `{}help ytadd` for more details.'.format(message.author.name, base.config['invoker']))
        return

    vcuser = discord.utils.get(message.server.members, id=musicbots[message.server.id]['bot_id'])

    if not vcuser:
        await client.send_message(message.channel, '🚫 {0}: **An unexpected error occurred:** The music bot for this server was not found. Please try again or change the music bot\'s id with `{1}ytadd {1}setup`. Use `{1}help ytadd` for more information.'.format(
            message.author.name,
            base.config['invoker']
            ))
        return

    vcchannel = vcuser.voice_channel

    if not vcchannel:
        await client.send_message(message.channel, '🚫 {}: The music bot is not connected to any voice channels.'.format(message.author.name))
        return

    if message.author.voice_channel != vcchannel:
        await client.send_message(message.channel, '🚫 {}: I cannot allow you to queue music to the music bot unless you are in the channel it is in as well.'.format(message.author.name))
        return

    query = message.content.split(None, 1)[1]

    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=5,
        type='video'
        ).execute()

    for search_result in search_response.get('items', []):
        await client.send_message(message.channel, 'I searched YouTube and got **{}**. Shall I add this video to the queue? (Reply **Y**es, **N**o, or **A**bort).\nhttp://youtu.be/{}'.format(search_result['snippet']['title'], search_result['id']['videoId']))

        while True:
            response = await client.wait_for_message(author=message.author, channel=message.channel)
            if response.content.lower() == 'yes' or response.content.lower() == 'y':
                if client.voice and client.voice.channel != vcchannel:
                    await client.voice.disconnect()
                    await client.join_voice_channel(vcchannel)
                if not client.voice:
                    await client.join_voice_channel(vcchannel)
                await client.send_message(message.channel, '{} http://youtu.be/{}'.format(musicbots[message.server.id]['invoker'], search_result['id']['videoId']))
                return
            elif response.content.lower() == 'no' or response.content.lower() == 'n':
                break
            elif response.content.lower() == 'abort' or response.content.lower() == 'a':
                await client.send_message(message.channel, 'Okay.')
                return
            else:
                await client.send_message(message.channel, 'Please say **Y**es, **N**o, or **A**bort.')

    await client.send_message(message.channel, '🚫 {}: You have exhausted my allotment of 5 results per search. Consider providing a more detailed query.'.format(message.author.name))

def resetstream():
    base.stream.stop()
    base.stream = None

@base.cacofunc
async def doommus(message, client):
    '''
    **{0}doommus** [ vc ]
    Sends a random DOOM song. If your command ends in `vc`, CacoBot will begin playing the song in the channel you are in.
    *Example: `{0}doommus vc`*
    '''
    song = choice(doommuse)

    if message.content.endswith('vc'):
        if base.stream:
            await client.send_message(message.channel, '🚫 {}: I\'m already playing some music in a voice channel. Please try again later.'.format(message.author.name))
            return

        if not message.author.voice_channel:
            await client.send_message(message.channel, '🚫 {}: You are not in a voice channel.'.format(message.author.name))
            return

        if client.voice and client.voice.channel != message.author.voice_channel:
            await client.voice.disconnect()
            await client.join_voice_channel(message.author.voice_channel)

        if not client.voice:
            await client.join_voice_channel(message.author.voice_channel)

        base.stream = await client.voice.create_ytdl_player(song, after=resetstream)

        base.stream.start()

    await client.send_message(message.channel, '{}: **{}**\n{}'.format(message.author.name, choice(doomsnark), song))
doommus.server = 'hidden'


@base.cacofunc
async def play(message, client):
    '''
    **{0}play** [ filename ]
    Plays a filename off my PC. Good fucking luck.
    *Example: `{0}play /mnt/sda2/Users/Orangestar/Music/Music/Truxton/Panic Protocol/01 Alexandrian Ricochet Sphere.mp3`*
    '''
    if base.stream:
        await client.send_message(message.channel, '🚫 {}: I\'m already playing some music in a voice channel. Please try again later.'.format(message.author.name))
        return

    if not message.author.voice_channel:
        await client.send_message(message.channel, '🚫 {}: You are not in a voice channel.'.format(message.author.name))
        return

    song = message.content.split(None, 1)[1]

    if not os.path.isfile(song):
        await client.send_message(message.channel, '🚫 {}: That file was not found.'.format(message.author.name))
        return

    if client.voice and client.voice.channel != message.author.voice_channel:
        await client.voice.disconnect()
        await client.join_voice_channel(message.author.voice_channel)

    if not client.voice:
        await client.join_voice_channel(message.author.voice_channel)

    base.stream = client.voice.create_ffmpeg_player(song, after=resetstream)

    base.stream.start()

    await client.send_message(message.channel, '{}: Now playing **{}** in {}'.format(message.author.name, song[song.rfind('/') + 1:], message.author.voice_channel))
doommus.server = 'hidden'
