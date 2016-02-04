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

games_list = [
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

# random game status
@asyncio.coroutine
def random_game():
    while True:
        yield from client.change_status(game=choice(games_list), idle=False)
        yield from asyncio.sleep(3600)

@client.async_event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #cacobot.radio.init()
    yield from random_game()

@client.async_event
def on_message(message):
    cont = True

    # execute Precommands
    for func in cacobot.base.pres:
        if cont == True:
            cont = yield from cacobot.base.pres[func](message, client)
        else:
            break

    if cont:
        if message.content.startswith(config['invoker']) and message.author.id != client.user.id: # ignore our own commands
            command = message.content[1:].split(' ')[0].lower() # So basically if the message was ".Repeat Butt talker!!!" this would be "repeat"
            if command in cacobot.base.functions:
                if message.channel.permissions_for(message.server.me).send_messages:
                    yield from client.send_typing(message.channel)
                    yield from cacobot.base.functions[command](message, client)
                else:
                    print('\n===========\nThe bot cannot send messages to #{} in the server "{}"!\n===========\n\nThis message is only showing up because I *tried* to send a message but it didn\'t go through. This probably means the mod team has tried to disable this bot, but someone is still trying to use it!\n\nHere is the command in question:\n\n{}\n\nThis was sent by {}.\n\nIf this message shows up a lot, the bot might be disabled in that server. You should just make it leave if the mod team isn\'t going to just kick it!'.format(message.channel.name, message.server.name, message.content, message.author.name))

        for func in cacobot.base.posts:
            yield from cacobot.base.posts[func](message, client)

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
        if args[0].author.id != client.user.id:
            if args[0].channel.is_private:
                print('This error was caused by a DM with {}.\n'.format(args[0].author))
            else:
                print('This error was caused by a message.\nServer: {}. Channel: #{}.\n'.format(args[0].server.name, args[0].channel.name))

            if sys.exc_info()[0].__name__ == 'ClientOSError' or sys.exc_info()[0].__name__ == 'ClientResponseError' or sys.exc_info()[0].__name__ == 'HTTPException':
                yield from client.send_message(args[0].channel, 'Sorry, I am under heavy load right now! This is probably due to a poor internet connection. Please submit your command again later.')
            elif sys.exc_info()[0].__name__ == 'Forbidden':
                yield from client.send_message(args[0].channel, 'You told me to do something that requires permissions I currently do not have. Ask an administrator to give me a proper role or something!')
            else:
                yield from client.send_message(args[0].channel, '{}\n{}: You caused {} **{}** with your command.'.format(
                    choice(hilarious_snark),
                    args[0].author.mention,
                    aan(sys.exc_info()[0].__name__),
                    sys.exc_info()[0].__name__)
                )
        else:
            yield from client.send_message(args[0].channel, 'Whoops, sorry, I nearly recursed just then! Sorry about that!')

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
