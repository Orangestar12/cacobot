import cacobot.base as base
import json, discord, traceback
from random import choice

# Open the config to get owner id.
with open('configs/config.json') as data:
    config = json.load(data)

@base.cacofunc
def memo(message, client, *args, **kwargs):
    '''
    **.memo** [add|remove]
    Allows you to add or remove yourself from the memoing system.
    If you are on the memoing system and you are mentioned in a channel that this bot is in, and you are not online, this bot will DM you where the mention was recieved (server and channel) plus the last 5 messages in that channel for context.
    *Example: `.memo add`*
    '''

    try:
        cmd = message.content.split(' ')[1]

        # Load memo list. This is created automatically when a mention is
        # in a message.
        with open('configs/memos.json') as data:
            memos = json.load(data)

        if cmd == 'add':
            if message.author.id not in memos:
                memos.append(message.author.id)
                yield from client.send_message(message.author,':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when you are mentioned.')
            else:
                yield from client.send_message(message.author,':no_entry_sign: You are already on the memo list.')
        elif cmd == 'remove':
            if message.author.id in memos:
                memos.remove(message.author.id)
                yield from client.send_message(message.author,':no_bell: You have been removed from the memo list.')
            else:
                yield from client.send_message(message.author,':no_entry_sign: You are not on the memo list.')
        else:
            raise(IndexError('User did not specify a valid command.')) # Boy howdy am I lazy.

        # Save memo list.
        with open('configs/memos.json', 'w') as data:
            json.dump(memos, data, indent=4)

    except IndexError:
        yield from client.send_message(message.channel, ':no_entry_sign: You must specify wether I should **add** or **remove** you from the memo list.')

@base.cacofunc
def hush(message, client, *args, **kwargs):
    '''
    **.hush** [server]
    Disables this bot from listening for commands in this channel. If [server] is supplied, extends the hush to the entire server.
    You can only call this command if you are able to kick.
    *Example: `.hush server`*
    '''

    # Do not continue if user does not have kick permissions.
    if message.channel.permissions_for(message.author).kick_members:

        # Load hush list. This is created automatically on the first message
        # received.
        with open('configs/hush.json') as data:
            hushed = json.load(data)

        # Server hush
        if message.content == '.hush server':
            hushed[message.server.id] = 'server'
            yield from client.send_message(message.channel, ':mute: **Server hush!** :mute:\n' + message.author.mention + ': I will no longer respond to commands in this server. Call `.listen` if you want me back. Ask Orangestar to remove me if you want me gone permanently.')

        # Channel hush
        else:
            hushed[message.channel.id] = 'channel'
            yield from client.send_message(message.channel, ':mute: **Channel hush!** :mute:\n' + message.author.mention + ': I will no longer respond to commands in this channel. Call `.listen` if you want to bring me back. Call `.hush server` if you were hoping to silence me on the whole server. (Hint: Do it somewhere I can hear it since you silenced me here.)')

        # Save hush list.
        with open('configs/hush.json', 'w') as data:
            json.dump(hushed, data, indent=4)
    else:
        yield from client.send_message(message.channel, ':no_entry_sign: {} You do not have permission to call this command.'.format(message.author.mention))

# People be like "Hey why can't we mention specific roles like mods?" and I add
# it to my bot and then it gets spammed as expected.
# Boy howdy Discord, aren't you a good community.

# @base.cacofunc # Uncomment this line to add it back.
def call(message, client, *args, **kwargs):
    '''
    **.call** [*role*]
    Mentions everyone in the role [*role*]. This is primarily for notifying mods that are away.
    *Example: `.call Mods`*
    '''

    roleToMention = message.content.split(' ', 1)[1].lower()

    if roleToMention != '@everyone':
        mentions = [] # holds mention strings
        for x in message.server.roles:
            if x.name.lower() == roleToMention:
                for y in message.server.members:
                    if discord.utils.find(lambda m: m == x, y.roles) != None:
                        mentions.append(y.mention)
        # Yeah, that *is* a shitty way of doing it.

        if mentions:
            yield from client.send_message(message.channel, '{}, you have been mentioned by {}!'.format(', '.join(mentions), message.author.mention))
        else:
            yield from client.send_message(message.channel, '{}: Nobody in this server has that role.'.format(message.author.mention))
    else:
        yield from client.send_message(message.channel, '{}: You have already mentioned everyone in that role.'.format(message.author.mention))

@base.cacofunc
def connect(message, client, *args, **kwargs):
    '''
    **.connect** [*invite*]
    Allows this bot to join your server.
    *Example: `.connect http://discord.gg/0iLJFytdVRBR1vgh`*
    *Please consider reading the Terms of Service for CacoBot before call `.connect`.*
    https://github.com/Orangestar12/cacobot/blob/master/tos.md
    '''
    try:
        yield from client.accept_invite(message.content.split(' ')[1])
        yield from client.send_message(message.channel, ':heart: I have successfully joined your server.')
    except discord.errors.NotFound:
        yield from client.send_message(message.channel, ':no_entry_sign: That was not a valid channel invite or id.')
    except:
        yield from client.send_message(message.channel, ':no_entry_sign: Your input was invalid. I have saved the traceback to my log. Please notify the bot maintainer immediately.')
        print(traceback.format_exc())

@base.cacofunc
def debug(message, client, *args, **kwargs):
    '''
    **.debug** [*command*]
    *This is a debug command. Only the bot owner can use it.*
    '''

    if message.author.id == config['owner_id']:
        cfgs = {}

        for x in [['configs/config.json', 'config'], ['configs/hush.json', 'hush'], ['configs/memos.json', 'memos'], ['configs/plugs.json', 'plugs'], ['configs/quotes.json', 'quotes'], ['configs/tags.json', 'tags']]:
            try:
                with open(x[0]) as data:
                    cfgs[x[1]] = json.load(data)
            except:
                pass
        yield from client.send_message(message.channel, '```\n{}\n```'.format(eval(message.content.split(' ', 1)[1])))
    else:
        yield from client.send_message(message.channel, ':no_entry_sign: You are not authorized to perform that command.')

@base.cacofunc
def plug(message, client, *args, **kwargs):
    '''
    **.plug** [*mention*]
    Makes this bot stop listening to a specific user. Only users that can kick can plug and unplug.
    *Example: `.plug @BooBot`*
    '''

    if message.author.id == config['owner_id'] or message.channel.permissions_for(message.author).kick_members:
        if message.author.id == config['owner_id'] and message.content.split(' ')[1] == 'GLOBAL':
            srv = 'GLOBAL'
        else:
            srv = message.server.id
        with open('configs/plugs.json') as data:
            plugs = json.load(data)
        for mention in message.mentions:
            plugs[mention.id] = srv
            yield from client.send_message(message.channel, ':heavy_check_mark: {} has been plugged.'.format(mention.name))
        with open('configs/plugs.json', 'w') as data:
            json.dump(plugs, data, indent=4)
    else:
        yield from client.send_message(message.channel, ':no_entry_sign: You are not authorized to perform that command.')

@base.cacofunc
def unplug(message, client, *args, **kwargs):
    '''
    **.unplug** [*mention*]
    Makes this bot resume listen to a user that has been plugged. Only users that can kick can plug and unplug.
    *Example: `.unplug @Orangestar`*
    '''

    if message.author.id == config['owner_id'] or message.channel.permissions_for(message.author).kick_members:
        with open('configs/plugs.json') as data:
            plugs = json.load(data)
        for mention in message.mentions:
            plugs.pop(mention.id)
            yield from client.send_message(message.channel, ':heavy_check_mark: {} has been unplugged.'.format(mention.name))
        with open('configs/plugs.json', 'w') as data:
            json.dump(plugs, data, indent=4)
    else:
        yield from client.send_message(message.channel, ':no_entry_sign: You are not authorized to perform that command.')

@base.cacofunc
def git(message, client, *args, **kwargs):
    '''
    **.git** [*file*]
    Sends a link to the CacoBot repo on Github. Provide [*file*] to link to a specific file. This is naive.
    *Example: `.git cacobot/changes.py`*
    '''
    snark = [
        'Stare into the abyss, and the abyss will stare back at you.',
        'Like, comment, and subscribe.',
        'Stick your head in it.',
        'Now browsing code on NIGHTMARE difficulty!',
        'Ohhhhhhhhhhhhhh yeeeeeeeeeeeessssssss!',
        '*Nervous coughing*'
    ]
    if message.content.strip() == '.git':
        yield from client.send_message(message.channel, '{}\nhttps://github.com/Orangestar12/cacobot/'.format(choice(snark)))
    else:
        yield from client.send_message(message.channel, '{}\nhttps://github.com/Orangestar12/cacobot/blob/master/{}'.format(choice(snark), message.content.split(' ')[1]))

@base.cacofunc
def myid(message,client, *args, **kwargs):
    '''
    **.myid**
    Returns your Discord ID for when another bot can't for some reason.
    *Example: `.myid`*
    '''
    yield from client.send_message(message.channel, '{}: Your ID is `{}`.'.format(message.author.mention, message.author.id))
