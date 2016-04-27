import os
import json
import random

#import youtube_dl

import cacobot.base as base

def resetstream():
    base.stream.stop()
    base.stream = None

@base.cacofunc
async def play(message, client):
    '''
    **{0}play** [ filename ]
    Plays a filename off my PC. Good fucking luck.
    *Example: `{0}play /mnt/sda2/Users/Orangestar/Music/Music/Truxton/Panic Protocol/01 Alexandrian Ricochet Sphere.mp3`*
    '''
    if base.stream:
        await client.send_message(message.channel, '\U0001F6AB {}: I\'m already playing some music in a voice channel. Please try again later.'.format(message.author.name))
        return

    if not message.author.voice_channel:
        await client.send_message(message.channel, '\U0001F6AB {}: You are not in a voice channel.'.format(message.author.name))
        return

    song = message.content.split(None, 1)[1]

    if not os.path.isfile(song):
        await client.send_message(message.channel, '\U0001F6AB {}: That file was not found.'.format(message.author.name))
        return

    if client.voice and client.voice.channel != message.author.voice_channel:
        await client.voice.disconnect()
        await client.join_voice_channel(message.author.voice_channel)

    if not client.voice:
        await client.join_voice_channel(message.author.voice_channel)

    base.stream = client.voice.create_ffmpeg_player(song, after=resetstream)

    base.stream.start()

    await client.send_message(message.channel, '{}: Now playing **{}** in {}'.format(message.author.name, song[song.rfind('/') + 1:], message.author.voice_channel))
play.server = 'hidden'

# Load radio list
try:
    with open('configs/songs.json') as Z:
        songs = json.load(Z)
# Create tags if not found
except FileNotFoundError:
    with open('configs/songs.json', 'w') as Z:
        Z.write('[]')
        songs = []

musicqueue = []
skips = []

currentsong = None

async def rdo(client):
    async def rd():
        global currentsong
        global skips

        if musicqueue:
            currentsong = musicqueue[0]
            musicqueue.pop(0)
        else:
            currentsong = random.randint(0, len(songs) - 1)

        base.stream = client.voice.create_ffmpeg_player(songs[currentsong]['location'], after=rd)
        base.stream.start()
        skips = []
    await rd()

@base.cacofunc
async def nowplaying(message, client):
    if currentsong:
        await client.send_message(message.channel, '\U0001F3B5 {}: Now playing: **{}**\n*Added by {}*'.format(message.author.name, songs[currentsong]['name'], songs[currentsong]['user']))
        return
    await client.send_message(message.channel, '\U0001F6AB {}: I am not playing any music.'.format(message.author.name))

whitelist = [
    '120205773425868804'
]

@base.cacofunc
async def radioon(message, client):
    '''
    **{0}summon**
    Makes this bot join your voice channel and start the radio.
    *Example: `{0}summon`*
    '''
    if message.server.id not in whitelist:
        await client.send_message(message.channel, '\U0001F6AB {}: Sorry, but your server is not in the radio whitelist.'.format(message.author.name))
        return

    if base.stream:
        await client.send_message(message.channel, '\U0001F6AB {}: I\'m already playing some music in a voice channel. Please try again later.'.format(message.author.name))
        return

    if not message.author.voice_channel:
        await client.send_message(message.channel, '\U0001F6AB {}: You are not in a voice channel.'.format(message.author.name))
        return

    if client.voice and client.voice.channel != message.author.voice_channel:
        await client.voice.disconnect()
        await client.join_voice_channel(message.author.voice_channel)

    if not client.voice:
        await client.join_voice_channel(message.author.voice_channel)

    await rdo(client)
radioon.server = 'hidden'

@base.cacofunc
async def radio(message, client):
    '''
    **{0}radio** *[ options ]*
    Provides interface for controlling the radio.
    **Options:**
    `add`, `play`, `skip`, `search`, `expunge`
    Use `{0}radio help option` for more information on an option.
    '''
    params = message.content.split()

    # just `.radio`
    if len(params) == 1:
        await client.send_message(
            message.channel,
            '\U0001F6AB {0}: You did not specify any options. Please use `{1}help tag` or `{1}tag help option` for more information.'.format(
                message.author.name,
                base.config['invoker']
                )
            )
        return

    if params[1] == 'help':

        # Response was valid
        if len(params) > 2 and params[2] in {'add', 'play', 'skip', 'search', 'expunge'}:

            if params[2] == 'add':
                await client.send_message(
                    message.channel,
                    '{}: `{}radio add <link>`\nAdds a song to the radio and queues it up to play next.'.format(
                        message.author.name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'play':
                await client.send_message(
                    message.channel,
                    '{}: `{}radio play <link>`\nQueues up a song to play next, but skips adding it to the standard radio playlist.'.format(
                        message.author.name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'skip':
                await client.send_message(
                    message.channel,
                    '{}: `{}radio skip`\nVotes to skip the song. This takes effect after /u2153rd of the channel votes to skip.'.format(
                        message.author.name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'search':
                await client.send_message(
                    message.channel,
                    '{}: `{}radio search <song name>`\nChecks the database songs with a given substring in their name, and asks if you wanted to queue it up next.'.format(
                        message.author.name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'expunge':
                await client.send_message(
                    message.channel,
                    '{}: `{}radio expunge <song id>`\nVotes to remove a song from the radio playlist. After 10 unique votes, the song will be removed.'.format(
                        message.author.name,
                        base.config['invoker']
                        )
                    )
                return

        # Response was invalid
        await client.send_message(
            message.channel,
            '{}: That is not a valid option for `{}radio`.'.format(
                message.author.name,
                base.config['invoker']
                )
            )
        return
    # end help

    #if params[1] == 'add':
        #if message.content.split()
radio.server = 'hidden'

@base.cacofunc
async def playlist(message, client):
    if message.author.id == '81088087249125376':
        await client.send_message(message.channel, '!playlist')
playlist.server = 'hidden'
