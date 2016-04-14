import inspect # To pretty-print docstrings

# for reading github api
import json
import urllib.request
import urllib.parse

import cacobot.base as base

# Please place the latest date you want the bot to check for commits:
# format is YYYY-MM-DDTHH:MM:SSZ
comdate = '2016-04-13'

@base.cacofunc
async def help(message, client): # pylint: disable=W0622
    '''
    *Cheeky, ain't ya?*
    **{0}help** [*cmd*]
    Displays a list of commands. If [*cmd*] is supplied, provides help about a specific command.
    *Example: `{0}help help`*
    '''

    params = message.content.split()
    if len(params) == 1:
        msg = 'These are my commands:\n'

        dect = {} # Oh god here we go

        for x in base.functions: # in with dictionaries gives keys, which are strings.
            # If a function is based upon a specific server (defined by a function's "server" attribute, which it may or may not have)
            if hasattr(base.functions[x], 'server'):
                if base.functions[x].server != 'hidden':
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

        msg += 'Use `{0}help [`*`command`*`]` to get more information about a command. **Please look up the help string for a command before using it or asking questions about it. Thank you!**'.format(
            base.config['invoker']
            )
        await client.send_message(message.channel, msg)
    else:
        if params[1] in base.functions:
            # check for docstring
            if base.functions[params[1]].__doc__:
                # Use inspect.getdoc() to clean the docstring up.
                await client.send_message(message.channel, inspect.getdoc(base.functions[params[1]]).format(
                    base.config['invoker'],
                    base.config['git']['repo_author'],
                    base.config['git']['repo_name']
                ))
            else:
                await client.send_message(message.channel, ':heavy_exclamation_mark: This command has no docstring! Go tell Orangestar that it\'s broken.')
        else:
            for x in base.functions:
                if hasattr(base.functions[x], 'server') and params[1].lower() == base.functions[x].server.lower():
                    await client.send_message(message.channel, '{}: ...Why did you just try to look up the help for a command category? I tried to split up the help message into categories so they could be read easier. Those big headers with the underlines and everything? Those are *categories*. There isn\'t a command called {}. (Why do so many people get this wrong? It\'s infuriating.)\n\n*~Orangestar, Bot maintainer.*'.format(
                        message.author.name,
                        params[1]
                        ))
                    return
            await client.send_message(message.channel, ':no_entry_sign: That command does not exist.')

# provide short information if mentioned.
@base.postcommand
async def welcome(message, client):
    if not message.channel.is_private and message.server.me in message.mentions:
        await client.send_message(
            message.channel,
            '{0}: For information on this bot, type `{1}help`. I don\'t log messages unless asked. Also, check out the `{1}git` command for my TOS and code.'.format(
                message.author.name,
                base.config['invoker']
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
        commsg = x['commit']['message'].split('\n')[0]
        if len(commsg) > 40:
            commsg = commsg[:40]
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
