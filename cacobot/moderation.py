import json
import traceback
import random

import discord
import cacobot.base as base

# Open the config to get owner id.
with open('configs/config.json') as data:
    config = json.load(data)

@base.cacofunc
async def hush(message, client):
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
        with open('configs/hush.json') as z:
            hushed = json.load(z)

        # Server hush
        if message.content == '.hush server':
            hushed[message.server.id] = 'server'
            await client.send_message(
                message.channel,
                ':mute: **Server hush!** :mute:\n{} will no longer respond to \
                commands in this server. Call `.listen` if you want me back. \
                Ask Orangestar to remove me if you want me gone permanently.'.format(
                    message.author.name
                    )
                )

        # Channel hush
        else:
            hushed[message.channel.id] = 'channel'
            await client.send_message(
                message.channel,
                ':mute: **Channel hush!** :mute:\n{}: I will no longer respond \
                to commands in this channel. Call `.listen` if you want to \
                bring me back. Call `.hush server` if you were hoping to \
                silence me on the whole server. (Hint: Do it somewhere I can \
                hear it since you silenced me here.)'.format(message.author.name)
                )

        # Save hush list.
        with open('configs/hush.json', 'w') as z:
            json.dump(hushed, z, indent=4)
    else:
        await client.send_message(
            message.channel,
            ':no_entry_sign: {} You do not have permission to call this command.'.format(
                message.author.mention
                )
            )

@base.precommand
async def checkForHush(message, client):
    '''
    Checks 'hush.json' to see if this server/channel shouldn't let the bot respond to commands.
    '''

    hushed = {}
    try:
        with open('configs/hush.json') as z:
            hushed = json.load(z)
    except FileNotFoundError: # Create hushed.json if it doesn't exist
        with open('configs/hush.json', 'w') as z:
            z.write('{}')

    # In retrospect this next bit could probably be a seperate function.
    if\
     not message.channel.is_private and\
     message.server.id in hushed and\
     hushed[message.server.id] == 'server':
        if message.content.startswith(config['invoker'] + 'listen'):
            hushed.pop(message.server.id)
            await client.send_message(
                message.channel,
                ':loud_sound: **Now listening!** :loud_sound:\n{}: I will now \
                respond to commands in this channel.'.format(
                    message.author.mention
                    )
                )
            with open('configs/hush.json', 'w') as z:
                json.dump(hushed, z, indent=4)
        return False

    elif\
     not message.channel.is_private and\
     message.channel.id in hushed and\
     hushed[message.channel.id] == 'channel':
        if message.content.startswith(config['invoker'] + 'listen'):
            hushed.pop(message.channel.id)
            await client.send_message(
                message.channel,
                ':loud_sound: **Now listening!** :loud_sound:\n{}: I will now \
                respond to commands in this channel.'.format(
                    message.author.mention
                    )
                )
            with open('configs/hush.json', 'w') as z:
                json.dump(hushed, z, indent=4)
        return False

    else:
        # Continue on to the command if we're not hushed.
        return True

@base.cacofunc
async def listen(message, client):
    '''
    **.listen**
    Cancels a hush. Applies to a channel, server, or both, depending on where it's called. This is the only command that works even if CacoBot is hushed.
    '''

    # This command doesn't actually do anything: It's a dummy to trigger
    # the actual .listen magic that's coded into inlinehush above.

    await client.send_message(
        message.channel,
        ':no_entry_sign: I am not hushed in this channel.'
        )

# People be like "Hey why can't we mention specific roles like mods?" and I add
# it to my bot and then it gets spammed as expected.
# Boy howdy Discord, aren't you a good community.

# @base.cacofunc # Uncomment this line to add it back.
async def call(message, client):
    '''
    **.call** [*role*]
    Mentions everyone in the role [*role*]. This is primarily for notifying mods that are away.
    *Example: `.call Mods`*
    '''

    roleToMention = message.content.split(None, 1)[1].lower()

    if roleToMention != '@everyone':
        mentions = [] # holds mention strings
        for x in message.server.roles:
            if x.name.lower() == roleToMention:
                for y in message.server.members:
                    if discord.utils.find(lambda m: m == x, y.roles) != None:
                        mentions.append(y.mention)
        # Yeah, that *is* a shitty way of doing it.

        if mentions:
            await client.send_message(
                message.channel,
                '{}, you have been mentioned by {}!'.format(
                    ', '.join(mentions),
                    message.author.mention
                    )
                )
        else:
            await client.send_message(
                message.channel,
                '{}: Nobody in this server has that role.'.format(
                    message.author.mention
                    )
                )
    else:
        await client.send_message(
            message.channel,
            '{}: You have already mentioned everyone in that role.'.format(
                message.author.mention
                )
            )

@base.cacofunc
async def connect(message, client):
    '''
    **.connect** [*invite*]
    Allows this bot to join your server.
    *Example: `.connect http://discord.gg/0iLJFytdVRBR1vgh`*
    *Please consider reading the Terms of Service for CacoBot before call `.connect`.*
    https://github.com/Orangestar12/cacobot/blob/master/tos.md
    '''
    try:
        await client.accept_invite(message.content.split()[1])
        await client.send_message(
            message.channel,
            ':heart: I have successfully joined your server.'
            )
    except discord.errors.NotFound:
        await client.send_message(
            message.channel,
            ':no_entry_sign: That was not a valid channel invite or id.'
            )
    except:
        await client.send_message(
            message.channel,
            ':no_entry_sign: Your input was invalid. I have saved the traceback to my log. Please notify the bot maintainer immediately.'
            )
        print(traceback.format_exc())

@base.cacofunc
async def debug(message, client):
    '''
    **.debug** [await | exec | *command*]
    *This is a debug command. Only the bot owner can use it.*
    '''

    if message.author.id == config['owner_id']:
        cfgs = {}

        for x in [
                ['configs/config.json', 'config'],
                ['configs/hush.json', 'hush'],
                ['configs/memos.json', 'memos'],
                ['configs/plugs.json', 'plugs'],
                ['configs/quotes.json', 'quotes'],
                ['configs/tags.json', 'tags']
        ]:
            try:
                with open(x[0]) as z:
                    cfgs[x[1]] = json.load(z)
            except FileNotFoundError:
                pass

        cmd = message.content.split(None, 1)[1].strip()
        if cmd.startswith('await'):
            response = await eval(message.content.split(None, 2)[2])
        elif cmd.startswith('exec'):
            exec(message.content.split(None, 2)[2])
            response = False
        else:
            response = eval(message.content.split(None, 1)[1])

        if response:
            await client.send_message(
                message.channel,
                '```\n{}\n```'.format(response)
                )
    else:
        await client.send_message(
            message.channel,
            ':no_entry_sign: You are not authorized to perform that command.'
            )

@base.cacofunc
async def plug(message, client):
    '''
    **.plug** [*mention*]
    Makes this bot stop listening to a specific user. Only users that can kick can plug and unplug.
    *Example: `.plug @BooBot`*
    '''

    if message.author.id == config['owner_id'] or\
            message.channel.permissions_for(message.author).kick_members:
        if message.author.id == config['owner_id'] and\
                message.content.split()[1] == 'GLOBAL':
            srv = 'GLOBAL'
        else:
            srv = message.server.id
        with open('configs/plugs.json') as z:
            plugs = json.load(z)
        for mention in message.mentions:
            plugs[mention.id] = srv
            await client.send_message(
                message.channel,
                ':heavy_check_mark: {} has been plugged.'.format(mention.name)
                )
        with open('configs/plugs.json', 'w') as z:
            json.dump(plugs, z, indent=4)
    else:
        await client.send_message(
            message.channel,
            ':no_entry_sign: You are not authorized to perform that command.'
            )

@base.cacofunc
async def unplug(message, client):
    '''
    **.unplug** [*mention*]
    Makes this bot resume listen to a user that has been plugged. Only users that can kick can plug and unplug.
    *Example: `.unplug @Orangestar`*
    '''

    if message.author.id == config['owner_id'] or \
            message.channel.permissions_for(message.author).kick_members:
        with open('configs/plugs.json') as z:
            plugs = json.load(z)
        for mention in message.mentions:
            plugs.pop(mention.id)
            await client.send_message(
                message.channel,
                ':heavy_check_mark: {} has been unplugged.'.format(mention.name)
                )
        with open('configs/plugs.json', 'w') as z:
            json.dump(plugs, z, indent=4)
    else:
        await client.send_message(
            message.channel,
            ':no_entry_sign: You are not authorized to perform that command.'
            )

@base.precommand
async def checkForPlug(message, client):
    if message.content.startswith(config['invoker']) and\
            message.content.split()[0][1:] in base.functions and\
            message.author.id != client.user.id:
        plugs = {}
        try:
            with open('configs/plugs.json') as z:
                plugs = json.load(z)
        except FileNotFoundError: # Create plugs.json if it doesn't exist
            with open('configs/plugs.json', 'w') as z:
                z.write('{}')

        if message.author.id in plugs and (\
                plugs[message.author.id] == 'GLOBAL' or\
                plugs[message.author.id] == message.server.id\
                ):
            await client.send_message(
                message.channel,
                '{}: Sorry, but you have been plugged.'.format(
                    message.author.mention
                    )
                )
            return False
    return True

@base.cacofunc
async def git(message, client):
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
        await client.send_message(
            message.channel,
            '{}\nhttps://github.com/Orangestar12/cacobot/'.format(
                random.choice(snark)
                )
            )
    else:
        await client.send_message(
            message.channel,
            '{}\nhttps://github.com/Orangestar12/cacobot/blob/master/{}'.format(
                random.choice(snark),
                message.content.split()[1]
                )
            )

@base.cacofunc
async def myid(message, client):
    '''
    **.myid**
    Returns your Discord ID for when another bot can't for some reason.
    *Example: `.myid`*
    '''
    await client.send_message(
        message.channel,
        '{}: Your ID is `{}`.'.format(message.author, message.author.id)
        )


@base.cacofunc
async def nuke(message, client):
    '''
    **.nuke** [*number*]
    Removes *number* amount of posts from the channel. If no number is specified, removes 20. This does not include your `.nuke` command.
    You can only call this command if you can remove posts yourself.
    *Example: `.nuke 20`*
    '''

    # r = number of requested deletions

    try:
        r = int(message.content.split(" ", 1)[1]) + 1
    except (ValueError, IndexError):
        r = 21

    if message.channel.permissions_for(message.author).manage_messages:
        if message.channel.permissions_for(
                discord.utils.get(
                    message.server.members,
                    id=client.user.id
                    )
        ).manage_messages:
            try:
                async for msg in client.logs_from(message.channel, r):
                    await client.delete_message(msg)
            except discord.errors.NotFound:
                pass
        else:
            await client.send_message(
                message.channel,
                ':no_entry_sign: I do not have permissions to delete messages \
                yet, so I cannot perform this command.'
                )
    else:
        await client.send_message(
            message.channel,
            ':no_entry_sign: Sorry, but I can\'t let you delete messages if \
            you don\'t have the permission to.'
            )

@base.cacofunc
async def cleanup(message, client):
    '''
    **.cleanup** [*number*]
    Removes *number* amount of posts by CacoBot from the channel, plus the invokers, for up to the last 100 messages. If no number is specified, removes 5.
    You can only call this command if you can remove posts yourself.
    *Example: `.cleanup 20`*
    '''

    # c = number of commands
    # r = number of requested deletions

    c = 0

    try:
        r = int(message.content.split(" ", 1)[1]) + 1
    except (ValueError, IndexError):
        r = 6

    if message.channel.permissions_for(message.author).manage_messages:
        if message.channel.permissions_for(
                discord.utils.get(
                    message.server.members,
                    id=client.user.id
                    )
        ).manage_messages:
            try:
                async for msg in client.logs_from(message.channel, 100):
                    if (msg.author.id == client.user.id or\
                            (msg.content.lower().startswith(config['invoker']) and\
                            msg.content[1:].split(" ", 1)[0] in base.functions)) and\
                            c < r:
                        await client.delete_message(msg)
                        if msg.content.startswith(config['invoker']) and\
                                msg.content[1:].split(" ", 1)[0] in base.functions:
                            c = c + 1
            except discord.errors.NotFound:
                pass
        else:
            await client.send_message(
                message.channel,
                ':no_entry_sign: I do not have permissions to delete messages \
                yet, so I cannot perform this command.'
                )
    else:
        await client.send_message(
            message.channel, ':no_entry_sign: Sorry, but I can\'t let you \
            delete messages if you don\'t have the permission to.'
            )

# @base.cacofunc
async def chanuke(message, client):
    if message.channel.permissions_for(message.author).manage_channels:

        chsTodel = [channel for channel in message.server.channels\
            if channel.name == message.content.split(" ", 1)[1]]

        for x in chsTodel:
            await client.delete_channel(x)
    else:
        await client.send_message(
            message.channel,
            ":no_entry_sign: You do not have the proper permissions to manage \
            channels in this server."
            )
chanuke.server = 'hidden'

@base.cacofunc
async def remove(message, client):
    """
    **.remove**
    Removes all messages in the last 2000 posts by a user specified.
    This is currently under development, so only the bot owner can invoke it.
    *Example: `.remove Skulltrail`*
    """
    await client.delete_message(message)
    if message.author.id == config['owner_id']:
        async for x in client.logs_from(message.channel, 2000):
            if x.author.name == message.content.split()[1]:
                await client.delete_message(x)
