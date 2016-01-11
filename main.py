import sys, discord, json, traceback, asyncio
import cacobot
from random import choice

# What we use for what:
# sys is used for tracebaks in on_error.
# discord is obvious.
# json is used to load the config file.
# traceback is also used to print tracebacks. I'm a lazy ass.
# asyncio is because we're using the async branch of discord.py.
# https://github.com/Rapptz/discord.py/tree/async
# random.choice for choosing game ids

# A sample configs/config.json should be supplied.
with open('configs/config.json') as data:
    config = json.load(data)

# log in
client = discord.Client(max_messages=5000)

def aan(string):
    '''Returns "a" or "an" depending on a string's first letter.'''
    if string[0].lower() in 'aeiou':
        return 'an'
    else:
        return 'a'

new_games_list = [
    discord.Game(name='The Ultimate DOOM'),
    discord.Game(name='DOOM II: Hell On Earth'),
    discord.Game(name='TNT: Evilution'),
    discord.Game(name='The Plutonia Experiment'),
    discord.Game(name='Strife: Veteran Edition'),
    discord.Game(name='Heretic'),
    discord.Game(name='Hexen'),
    discord.Game(name='Hexen II'),
    discord.Game(name='Heretic 2'),
    discord.Game(name='Duke Nukem 3D'),
    discord.Game(name='Shadow Warrior'),
    discord.Game(name='Marathon'),
    discord.Game(name='Marathon: Durandal'),
    discord.Game(name='Marathon Infinity'),
    discord.Game(name='Blood'),
    discord.Game(name='Quake'),
    discord.Game(name='Quake II'),
    discord.Game(name='Quake III Arena')
]

old_games_list = [
    discord.Game(name='Doom 3'),
    discord.Game(name='Quake Live'),
    discord.Game(name='Quake'),
    discord.Game(name='Quake II'),
    discord.Game(name='Q3A'),
    discord.Game(name='Warsow'),
    discord.Game(name='Xonotic'),
    discord.Game(name='System Shock'),
    discord.Game(name='System Shock 2'),
    discord.Game(name='Strife: Veteran Edition'),
    discord.Game(name='Star Wars Jedi Knight'),
    discord.Game(name='Wolfenstein - Enemy Territory'),
    discord.Game(name='Unreal'),
    discord.Game(name='Alien Vs Predator, Thief')
]

# random game status
@asyncio.coroutine
def random_retro_game():
    while True:
        # Change currently-playing game to Doom 3, Quake Live, Quake, Quake II, Q3A, Warsow, Xonotic, System Shock, System Shock 2, Strife: Veteran Edition, Star Wars Jedi Knight, Star Wars Jedi Knight II, Wolfenstein - ET, Unreal, Alien Vs Predator, Thief (choices in that order)
        yield from client.change_status(game=choice(new_games_list), idle=False)
        yield from asyncio.sleep(3600)

@client.async_event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #cacobot.radio.init()
    yield from random_retro_game()
    # No ioquake or ZDoom or PrBoom+, but S:VE more than makes up for that.

@client.async_event
def on_message(message):
    # Check the list to see if this server/channel is hushed.
    hushed = {}
    try:
        with open('configs/hush.json') as data:
            hushed = json.load(data)
    except FileNotFoundError: # Create hushed.json if it doesn't exist
        with open('configs/hush.json', 'w') as data:
            json.dump(hushed, data, indent=4)

    # In retrospect this next bit could probably be a seperate function.
    if message.channel.is_private == False and message.server.id in hushed and hushed[message.server.id] == 'server':
        if message.content.startswith(config['invoker'] + 'listen'):
            hushed.pop(message.server.id)
            yield from client.send_message(message.channel, ':loud_sound: **Now listening!** :loud_sound:\n{}: I will now respond to commands in this channel.'.format(message.author.mention))
            with open('configs/hush.json', 'w') as data:
                json.dump(hushed, data, indent=4)

    elif message.channel.is_private == False and message.channel.id in hushed and hushed[message.channel.id] == 'channel':
        if message.content.startswith(config['invoker'] + 'listen'):
            hushed.pop(message.channel.id)
            yield from client.send_message(message.channel, ':loud_sound: **Now listening!** :loud_sound:\n{}: I will now respond to commands in this server.'.format(message.author.mention))
            with open('configs/hush.json', 'w') as data:
                json.dump(hushed, data, indent=4)

    # Continue on to the command if we're not hushed.
    # This code is pretty self-explanitory.
    else:

        plugs = {}
        try:
            with open('configs/plugs.json') as data:
                plugs = json.load(data)
        except FileNotFoundError: # Create plugs.json if it doesn't exist
            with open('configs/plugs.json', 'w') as data:
                json.dump(plugs, data, indent=4)

        if message.content.startswith(config['invoker']) and message.author.id != client.user.id: # ignore our own commands
            command = message.content[1:].split(' ')[0].lower() # So basically if the message was ".Repeat Butt talker!!!" this would be "repeat"
            if command in cacobot.base.functions:
                if message.author.id in plugs and (plugs[message.author.id] == 'GLOBAL' or plugs[message.author.id] == message.server.id):
                    yield from client.send_message(message.channel, '{}: Sorry, but you have been plugged.'.format(message.author.mention))
                else:
                    yield from client.send_typing(message.channel)
                    yield from cacobot.base.functions[command](message, client)

        # Print tag count.
        if message.content.startswith('Retrieving tags owned by') or message.content.startswith('I found these tags for the user:') or (not message.channel.is_private and message.content.startswith('Tags from ' + message.server.name)):
            msglist = message.content[message.content.index('\n')+1:].split(', ')
            yield from client.send_message(message.channel, message.author.mention + ': I calculated **{}** tags from that list.'.format(len(msglist)))

        if message.mentions: # False if no mentions
            # Load memo list
            memos = {}
            try:
                with open('configs/memos.json') as data:
                    memos = json.load(data)
            except FileNotFoundError:
                with open('configs/memos.json', 'w') as data:
                    json.dump(memos, data, indent=4)

            msgme = []

            for mention in message.mentions:
                # The async branch turned status into an enum. It's nice.
                # If the mentioned user is not online, signed up for memos, and is able to see the channel:
                if mention.id in memos and mention.status != discord.Status.online and message.channel.permissions_for(mention).read_messages:
                    # Store user for later messaging.
                    msgme.append(mention)

            # yield from is weird: You can only call it in specific
            # places. Here we reverse a log of the last 5 messages.
            if msgme:
                log = yield from client.logs_from(message.channel, 5)
                log = reversed(list(log))
                # If your net/computer is slow enough, sometimes you'll
                # get a few messages after the mention. Deal with it.
                msgToSend = '**You were mentioned in {}\'s #{} channel.** Here is the context:\n'.format(message.server.name, message.channel.name)

                # refer to log.py for info on how this works:
                for x in log:
                    minute = '00'
                    if len(str(x.timestamp.minute)) != 2:
                        minute = '0' + str(x.timestamp.minute)
                    else:
                        minute = str(x.timestamp.minute)
                    msgToSend += '{}:{} - {}: {}\n'.format(
                      str(x.timestamp.hour),
                      minute,
                      x.author.name,
                      x.content)

                for mention in msgme:
                    yield from client.send_message(mention, msgToSend[:1980]) # Really shitty way of making sure it's beneath 2k characters but IT WORKS, SO CAN IT
                    asyncio.sleep(5)

        if message.mention_everyone: # @everyone

            # Load memo list
            memos = {}
            try:
                with open('configs/memos.json') as data:
                    memos = json.load(data)
            except FileNotFoundError:
                with open('configs/memos.json', 'w') as data:
                    json.dump(memos, data, indent=4)

            msgme = []
            for mem in memos:
                # Find member object based on id
                usr = discord.utils.find(lambda x: x.id == mem, message.server.members)
                # Prevent mentions in cannels people can't read from being sent
                if usr != None and message.channel.permissions_for(usr).can_read_messages and usr.status != discord.Status.online:
                    msgme.append(usr)

            if msgme:
                log = yield from client.logs_from(message.channel, 5)
                log = reversed(list(log))

                msgToSend = '**Someone used \@everyone in {}\'s #{} channel.** Here is the context:\n'.format(message.server.name, message.channel.name)

                # refer to log.py for info on how this works:
                for x in log:
                    minute = '00'
                    if len(str(x.timestamp.minute)) != 2:
                        minute = '0' + str(x.timestamp.minute)
                    else:
                        minute = str(x.timestamp.minute)
                    msgToSend += '{}:{} - {}: {}\n'.format(
                      str(x.timestamp.hour),
                      minute,
                      x.author.name,
                      x.content)

                for mention in msgme:
                    yield from client.send_message(mention, msgToSend[:1980])
                    asyncio.sleep(5)

hilarious_snark = [
    'Good job. Nice work.',
    'You knew that was broken, didn\'t you?',
    'Abort? Retry? Fail?',
    '**HISSSSSSSSSSSSSSSSSSSS**',
    'wosh u code',
    'You IDIOT. You know what\'s going on here, don\'t you? You just wanted to see me suffer.',
    'WHAT AM I FIGHTING FOOOOOOOOOOOR?',
    'OH GUTS, IS IT MONSTER CLOSET TIME?',
    'I... failed you.',
    'I AM ERROR.',
    '`IDENTITY #14: YOU HAVE 5 SECONDS TO COMPLY.`',
    'ERROR: INSTRUCTED COMMAND CONFLICTS WITH DIRECTIVE 4.'
]

@client.async_event
def on_error(event, *args, **kwargs):
    # args[0] is the message that was recieved prior to the error. At least,
    # it should be. We check it first in case the cause of the error wasn't a
    # message.
    print('An error has been caught.')
    print(traceback.format_exc())
    if args and type(args[0]) == discord.Message:
        if args[0].channel.is_private:
            print('This error was caused by a DM with {}.\n'.format(args[0].author))
        else:
            print('This error was caused by a message.\nServer: {}. Channel: #{}.\n'.format(args[0].server.name, args[0].channel.name))

        if sys.exc_info()[0].__name__ == 'ClientOSError' or sys.exc_info()[0].__name__ == 'ClientResponseError':
            yield from client.send_message(args[0].channel, 'Sorry, I am under heavy load right now! This is probably due to a poor internet connection. Please submit your command again later.')
        else:
            yield from client.send_message(args[0].channel, '{}\n{}: You caused {} **{}** with your command.'.format(
                choice(hilarious_snark),
                args[0].author.mention,
                aan(sys.exc_info()[0].__name__),
                sys.exc_info()[0].__name__)
            )
            yield from client.send_message(args[0].channel, '```\n{}\n```'.format(traceback.format_exc()))

# I'm gonna be honest, I have *no clue* how asyncio works. This is all from the
# example in the docs.
def main_task():
    yield from client.login(config['email'], config['password'])
    yield from client.connect()

loop = asyncio.get_event_loop()
loop.run_until_complete(main_task())
loop.close()

# If you're taking the senic tour of the code, you should check out
# cacobot/__init__.py next.
