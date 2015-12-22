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

# random game status
@asyncio.coroutine
def random_retro_game():
    while True:
        # Change currently-playing game to Doom 3, Quake Live, Quake, Quake II, Q3A, Warsow, Xonotic, System Shock, System Shock 2, Strife: Veteran Edition, Star Wars Jedi Knight, Star Wars Jedi Knight II, Wolfenstein - ET, Unreal, Alien Vs Predator, Thief (choices in that order)
        yield from client.change_status(game_id=choice([712, 385, 482, 483, 484, 738, 815, 701, 534, 600, 601, 613, 635, 714, 822]), idle=False)
        yield from asyncio.sleep(3600)

@client.async_event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
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
        if message.content.startswith('.listen'):
            hushed.pop(message.server.id)
            yield from client.send_message(message.channel, ':loud_sound: **Now listening!** :loud_sound:\n{}: I will now respond to commands in this channel.'.format(message.author.mention))
            with open('configs/hush.json', 'w') as data:
                json.dump(hushed, data, indent=4)

    elif message.channel.is_private == False and message.channel.id in hushed and hushed[message.channel.id] == 'channel':
        if message.content.startswith('.listen'):
            hushed.pop(message.channel.id)
            yield from client.send_message(message.channel, ':loud_sound: **Now listening!** :loud_sound:\n{}: I will now respond to commands in this server.'.format(message.author.mention))
            with open('configs/hush.json', 'w') as data:
                json.dump(hushed, data, indent=4)

    # Continue on to the command if we're not hushed.
    # This code is pretty self-explanitory.
    else:

        plugs = []
        try:
            with open('configs/plugs.json') as data:
                plugs = json.load(data)
        except FileNotFoundError: # Create plugs.json if it doesn't exist
            with open('configs/plugs.json', 'w') as data:
                json.dump(plugs, data, indent=4)

        if message.content.startswith('.') and message.author.id != client.user.id: # ignore our own commands
            command = message.content[1:].split(' ')[0].lower() # So basically if the message was ".Repeat Butt talker!!!" this would be "repeat"
            if command in cacobot.base.functions:
                if message.author.id not in plugs:
                    yield from client.send_typing(message.channel)
                    yield from cacobot.base.functions[command](message, client)
                else:
                    yield from client.send_message(message.channel, '{}: Sorry, but you have been plugged.'.format(message.author.mention))

        # Print tag count.
        if message.content.startswith('Retrieving tags owned by'):
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
                # If the mentioned user is not online and signed up for memos:
                if mention.id in memos and mention.status != discord.Status.online:
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


@client.async_event
def on_error(event, *args, **kwargs):
    # args[0] is the message that was recieved prior to the error. At least,
    # it should be. We check it first in case the cause of the error wasn't a
    # message.
    if args and type(args[0]) == discord.Message:
        print(traceback.format_exc())
        yield from client.send_message(args[0].channel, 'Niiiice work, {}, you just caused {} **{}**!'.format(args[0].author.mention, aan(sys.exc_info()[0].__name__), sys.exc_info()[0].__name__))
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
