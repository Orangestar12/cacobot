import json # to load tags
import re # to find mentions
import asyncio # to sleep

import discord # for errors

import cacobot.base as base

mention_syntax = re.compile(r'(<@([0-9#]*?)>)')

# Load msgs
try:
    with open('configs/away.json') as Z:
        msgs = json.load(Z)
# Create away message file if not found
except FileNotFoundError:
    with open('configs/away.json', 'w') as Z:
        Z.write('{}')
        msgs = {}

@base.cacofunc
async def away(message, client):
    '''
    **{0}away** <message>
    Sets an away message, allowing this bot to automatically respond when you are mentioned.
    *Example: `.away I'm busy fending off this marine dude. DM me if you need me! `❤` `*
    '''
    global msgs # pylint: disable=W0602

    if len(message.content.split()) == 1:
        await client.send_message(message.channel, '{}: Please provide a message that I will respond with when you are mentioned.'.format(message.author.name))
        return

    msg = message.content.split(None, 1)[1].replace('@everyone', '@\u2020everyone')

    if mention_syntax.search(msg):
        await client.send_message(message.channel, '{}: To prevent abuse, you are not allowed to provide mentions in your away messages.'.format(message.author.name))
        return


    msgs[message.author.id] = {'msg' : msg, 'grossfix' : True, 'cooldown' : False}

    with open('configs/away.json', 'w') as z:
        json.dump(msgs, z, indent=4)

    try:
        await client.delete_message(message)
    except(discord.errors.NotFound, discord.Forbidden):
        pass

    await client.send_message(message.author, '{0}: I will now automatically respond with this message when you are mentioned:\n\n{0} is away. This is their set message:\n\n{1}\n\n*This is an automated response. You can set one up yourself with `.away`.*'.format(message.author.name, msg))

@base.postcommand
async def awayhelper(message, client):
    global msgs # pylint: disable=W0602

    if message.author.id in msgs and not msgs[message.author.id]['grossfix']:
        msgs.pop(message.author.id)

        with open('configs/away.json', 'w') as z:
            json.dump(msgs, z, indent=4)

        if message.channel.is_private:
            await client.send_message(message.author, '{}: Your away message has been automatically disabled.'.format(message.author.name))
        else:
            await client.send_message(message.author, '{}: Your away message has been automatically disabled because you sent a message in #{}'.format(message.author.name, message.channel.name))
    elif message.author.id in msgs and msgs[message.author.id]['grossfix']:
        msgs[message.author.id]['grossfix'] = False
        with open('configs/away.json', 'w') as z:
            json.dump(msgs, z, indent=4)

    if message.mentions:
        respond = [x for x in message.mentions if x.id in msgs]

        for x in respond:
            if not msgs[x.id]['cooldown']:
                await client.send_message(message.channel, '{}: {} is away. This is their set message:\n\n{}\n\n*This is an automated response. You can set one up yourself with `.away`.*'.format(message.author.name, x.name, msgs[x.id]['msg']))
                msgs[x.id]['cooldown'] = True
                await asyncio.sleep(30)
                msgs[x.id]['cooldown'] = False
