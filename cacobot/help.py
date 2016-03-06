import inspect # To pretty-print docstrings
import cacobot.base as base

@base.cacofunc
async def help(message, client):
    '''
    *Cheeky, ain't ya?*
    **.help** [*cmd*]
    Displays a list of commands. If [*cmd*] is supplied, provides help about a specific command.
    *Example: `.help help`*
    '''

    params = message.content.split(" ")
    if message.content.strip()[1:] == 'help':
        msg = 'These are my commands:\n'

        dect = {} # Oh god here we go

        for x in base.functions: # in with dictionaries gives keys, which are strings.
            # If a function is based upon a specific server (defined by a function's "server" attribute, which it may or may not have)
            if hasattr(base.functions[x], 'server'):
                # Append to a key with that server's name
                try:
                    dect[base.functions[x].server].append(x)
                except KeyError:
                    dect[base.functions[x].server] = []
                    dect[base.functions[x].server].append(x)
            else:
                try:
                    dect['all'].append(x)
                except KeyError:
                    dect['all'] = []
                    dect['all'].append(x)

        msg += '__**Global Commands**__\n'
        msg += ' '.join(sorted(dect['all']))
        msg += '\n\n'
        for x in sorted(dect):
            if x != 'all':
                msg += '__**{}**__\n'.format(x)
                msg += ' '.join(sorted(dect[x]))
                msg += '\n\n'

        msg += 'Use `.help [`*`command`*`]` to get more information about a command.\nUse `.welcome` if you are completely unsure of how to use this bot.'
        await client.send_message(message.channel, msg)
    else:
        if params[1] in base.functions:
            # check for docstring
            if base.functions[params[1]].__doc__:
                # Use inspect.getdoc() to clean the docstring up.
                await client.send_message(message.channel, inspect.getdoc(base.functions[params[1]]))
            else:
                await client.send_message(message.channel, ':heavy_exclamation_mark: This command has no docstring! Go tell Orangestar that it\'s broken.')
        else:
            await client.send_message(message.channel, ':no_entry_sign: That command does not exist.')

@base.cacofunc
async def welcome(message, client):
    '''
    **.welcome**
    Displays a helpful message about how to use CacoBot!
    *Example: `.welcome`*
    '''

    # You should customize this message to meet the standards of your own bot.

    await client.send_message(message.author, 'HISSSSSSS! I\'m **CacoBot** r22! I was made by **Orangestar** to help out with a Doom-related server, but now I roam Discord checking out the servers available. My purpose is to act as a *supplementary* bot to existing bots on your server. I\'m packing a bunch of weird, superfluous commands that keep me lightweight and don\'t obsolete other bots. You can check them out with the `.help` command! Some stuff you might be interested:\n\nUse `.log` to get a nice, copy-pastable copy of the last few messages in a channel to add to quotes or share with a friend.\n\nCheck out my Github repo and personal server with `.git`.\n\nI have a set of commands for saving hilarious quotes from other users! Log is perfect for adding quotes to this database. If you ever need a pick-me-up, call `.quote`!\n\nFor everything else, you should call `.help` for a list of commands and `.help [`*`command`*`]` for specific information about a specific command. Have fun!')

# If you're taking the senic tour of the code, you're free to look around as you
# please from this point on, though I recommend checking out configs/config.json

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
# change_list = [
#     ['all', 'This command is deprecated.']
# ]

# There's a few more emojis I could use for bullets, but these stuck out the most to me.
# emojis = [':black_small_square:', ':small_blue_diamond:', ':small_orange_diamond:', ':small_red_triangle:']

@base.cacofunc
async def changes(message, client):
    '''
    **.changes**
    Displays the most recent CacoBot changes.
    *This command is deprecated.*
    *Example: `.changes`*
    '''
    await client.send_message(message.channel, '{}: This command is deprecated. For most recent changes, check out the commits on the CacoBot GitHub.\nhttps://github.com/Orangestar12/cacobot/commits/master'.format(message.author.name))

    # printChanges = '{}: **Latest Changes**\n'.format(message.author.mention)
    #
    # for x in change_list:
    #     if message.channel.is_private:
    #         if x[0] == 'all':
    #             printChanges += '{} {} \n'.format(random.choice(emojis), x[1])
    #     else:
    #         if x[0] == 'all' or message.server.name == x[0]:
    #             printChanges += '{} {} \n'.format(random.choice(emojis), x[1])
    #
    # await client.send_message(message.channel, printChanges)
