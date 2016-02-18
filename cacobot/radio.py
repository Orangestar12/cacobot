import cacobot.base as base
import discord

channel = None

def init():
    discord.opus.load_opus() # I think?

@base.cacofunc
def radio(message, client, *args, **kwargs):

    params = message.split(None, 2)
    if message.content.strip()[1:] == 'radio':
        yield from client.send_message(message.channel, 'If you do not know how to use this command, call `.help radio`!')
    elif params[1] == 'connect':
        svToConnect = discord.utils.find(lambda x: x.name == params[2] and x.type = discord.ChannelType.voice, message.server.channels)
        if svToConnect == None:
            yield from client.send_message(message.channel, 'I could not connect to that channel.')
        else:
            yield from client.join_voice_channel(svToConnect)
