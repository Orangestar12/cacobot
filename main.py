# per-module import for actioninja

# standard imports
import sys # for tracebaks in on_error.
import json # to load the config file.
import traceback # also used to print tracebacks. I'm a lazy ass.
import asyncio # because we're using the async branch of discord.py.
from random import choice # for choosing game ids

import discord # obvious.
# https://github.com/Rapptz/discord.py/tree/async

import cacobot # imports all plugins in the cacobot folder.

# A sample configs/config.json should be supplied.
with open('configs/config.json') as data:
    config = json.load(data)

# log in
client = discord.Client(max_messages=100)

def aan(string):
    '''Returns "a" or "an" depending on a string's first letter.'''
    if string[0].lower() in 'aeiou':
        return 'an'
    else:
        return 'a'

# random game status
@asyncio.coroutine
def random_game():
    ''' Changes the game in the bot's status. '''
    while True:
        name = choice(config['games'])
        game = discord.Game(name=name)
        yield from client.change_status(game=game)
        yield from asyncio.sleep(3600)

@client.async_event
def on_ready():
    ''' Executed when the bot successfully connects to Discord. '''
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #cacobot.radio.init()
    yield from random_game()

@client.async_event
def on_message(message):
    '''
    Executed when the bot recieves a message.

    [message] is a discord.Message object, representing the sent message.
    '''
    cont = True

    # execute Precommands
    for func in cacobot.base.pres:
        if cont:
            cont = yield from cacobot.base.pres[func](message, client)
        else:
            break

    if cont:
        if message.content.startswith(config['invoker']) and \
        message.author.id != client.user.id: # ignore our own commands
            command = message.content[1:].split(' ')[0].lower()
            # So basically if the message was ".Repeat Butt talker!!!" this
            # would be "repeat"
            if command in cacobot.base.functions:
                if message.channel.is_private or\
                message.channel.permissions_for(message.server.me).send_messages:
                    yield from client.send_typing(message.channel)
                    yield from cacobot.base.functions[command](message, client)
                else:
                    print('\n===========\nThe bot cannot send messages to #{} in the server "{}"!\n===========\n\nThis message is only showing up because I *tried* to send a message but it didn\'t go through. This probably means the mod team has tried to disable this bot, but someone is still trying to use it!\n\nHere is the command in question:\n\n{}\n\nThis was sent by {}.\n\nIf this message shows up a lot, the bot might be disabled in that server. You should just make it leave if the mod team isn\'t going to just kick it!'.format(
                         message.channel.name,
                         message.server.name,
                         message.content,
                         message.author.name
                         )
                         )

        for func in cacobot.base.posts:
            yield from cacobot.base.posts[func](message, client)

@client.async_event
def on_error(*args):
    '''
    This event is basically a script-spanning `except` statement.
    '''
    # args[0] is the message that was recieved prior to the error. At least,
    # it should be. We check it first in case the cause of the error wasn't a
    # message.
    print('An error has been caught.')
    print(traceback.format_exc())
    if args and isinstance(args[0], discord.Message):
        if args[0].author.id != client.user.id:
            if args[0].channel.is_private:
                print('This error was caused by a DM with {}.\n'.format(args[0].author))
            else:
                print(
                    'This error was caused by a message.\nServer: {}. Channel: #{}.\n'.format(
                        args[0].server.name,
                        args[0].channel.name
                        )
                    )

            if \
             sys.exc_info()[0].__name__ == 'ClientOSError' or \
             sys.exc_info()[0].__name__ == 'ClientResponseError' or \
             sys.exc_info()[0].__name__ == 'HTTPException':
                yield from client.send_message(
                    args[0].channel,
                    'Sorry, I am under heavy load right now! This is probably due to a poor internet connection. Please submit your command again later.'
                    )
            elif sys.exc_info()[0].__name__ == 'Forbidden':
                yield from client.send_message(
                    args[0].channel,
                    'You told me to do something that requires permissions I currently do not have. Ask an administrator to give me a proper role or something!')
            else:
                yield from client.send_message(
                    args[0].channel,
                    '{}\n{}: You caused {} **{}** with your command.'.format(
                        choice(config['error_messages']),
                        args[0].author.mention,
                        aan(sys.exc_info()[0].__name__),
                        sys.exc_info()[0].__name__)
                    )

client.run(config['email'], config['password'])

# Here's the old manual-loop way of starting the bot.

# def main_task():
#     '''
#     I'm gonna be honest, I have *no clue* how asyncio works. This is all from
#     the example in the docs.
#     '''
#     yield from client.login(config['email'], config['password'])
#     yield from client.connect()
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main_task())
# loop.close()

# If you're taking the senic tour of the code, you should check out
# cacobot/__init__.py next.
