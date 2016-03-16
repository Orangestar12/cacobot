import inspect # To pretty-print docstrings

# for reading github api
import json
import urllib.request
import urllib.parse

import cacobot.base as base

# Please place the latest date you want the bot to check for commits:
# format is YYYY-MM-DDTHH:MM:SSZ
comdate = '2016-03-15'

@base.cacofunc
async def help(message, client):
    '''
    *Cheeky, ain't ya?*
    **{0}help** [*cmd*]
    Displays a list of commands. If [*cmd*] is supplied, provides help about a specific command.
    *Example: `{0}help help`*
    '''

    params = message.content.split(" ")
    if message.content.strip()[len(base.config['invoker']):] == 'help':
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

        msg += 'Use `{0}help [`*`command`*`]` to get more information about a command.'.format(
            base.config['invoker']
            )
        await client.send_message(message.channel, msg)
    else:
        if params[1] in base.functions:
            # check for docstring
            if base.functions[params[1]].__doc__:
                # Use inspect.getdoc() to clean the docstring up.
                await client.send_message(message.channel, inspect.getdoc(base.functions[params[1]]).format(
                    base.config['invoker']
                ))
            else:
                await client.send_message(message.channel, ':heavy_exclamation_mark: This command has no docstring! Go tell Orangestar that it\'s broken.')
        else:
            await client.send_message(message.channel, ':no_entry_sign: That command does not exist.')

#@base.cacofunc
# async def welcome(message, client):
    # '''
    # **{0}welcome**
    # Displays a helpful message about how to use CacoBot!
    # *Example: `{0}welcome`*
    # '''

    # You should customize this message to meet the standards of your own bot.

    # await client.send_message(message.author, 'HISSSSSSS! I\'m **CacoBot** r22! I was made by **Orangestar** to help out with a Doom-related server, but now I roam Discord checking out the servers available. My purpose is to act as a *supplementary* bot to existing bots on your server. I\'m packing a bunch of weird, superfluous commands that keep me lightweight and don\'t obsolete other bots. You can check them out with the `.help` command! Some stuff you might be interested:\n\nUse `.log` to get a nice, copy-pastable copy of the last few messages in a channel to add to quotes or share with a friend.\n\nCheck out my Github repo and personal server with `.git`.\n\nI have a set of commands for saving hilarious quotes from other users! Log is perfect for adding quotes to this database. If you ever need a pick-me-up, call `.quote`!\n\nFor everything else, you should call `.help` for a list of commands and `.help [`*`command`*`]` for specific information about a specific command. Have fun!')

# provide short information if mentioned.
@base.postcommand
async def welcome(message, client):
    if not message.channel.is_private and message.server.me in message.mentions:
        await client.send_message(
            message.channel,
            '{}: For information on this bot, type `.help`. I don\'t log messages. Also, check out the `.git` command for my TOS and code.'.format(
                message.author.name
                )
            )

@base.cacofunc
async def changes(message, client):
    '''
    **{0}changes**
    Displays the most recent changes to the bot's code. Commits directly from the maintainer appear in bold.
    *Example: `{0}changes`*
    '''

    # For this command to work, make sure you've authenticated with curl first:
    # curl -i -u your_username https://api.github.com/

    req = json.loads(urllib.request.urlopen(urllib.request.Request(
        'https://api.github.com/repos/{}/{}/commits?since={}'.format(
            base.config['git']['repo_author'],
            base.config['git']['repo_name'],
            comdate
            ),
        headers={
            'Accept' : 'application/vnd.github.v3+json'
            }
        )).read().decode('UTF-8'))

    msgToSend = '__**Recent commits from {} repository on GitHub:**__\n'.format(base.config['git']['repo_name'])

    for x in req:
        commsg = x['commit']['message'].replace('\n', '\n    ')
        if x['committer']['login'] == base.config['git']['repo_author']:
            msgToSend += '**{}:** {}'.format(x['committer']['login'], commsg)
        else:
            msgToSend += '{}: {}'.format(x['committer']['login'], commsg)
        msgToSend += '\n'

    msgToSend += 'https://github.com/{}/{}/commits/master'.format(base.config['git']['repo_author'], base.config['git']['repo_name'])

    if len(msgToSend) <= 2000:
        await client.send_message(message.channel, msgToSend)
    else:
        await client.send_message(message.channel, 'This is embarrasing, there\'s been so many changes to my code I can\'t print them all. You can always check the GitHub repo at https://github.com/{}/{}/commits/master for the latest updates.\n(Hey! Also, tell my owner "You have the date in help.py set too high"! Thanks.)'.format(base.config['git']['repo_author'], base.config['git']['repo_name']))

# If you're taking the senic tour of the code, you're free to look around as you
# please from this point on, though I recommend checking out configs/config.json
