import cacobot.base as base
import inspect # To pretty-print docstrings

@base.cacofunc
def help(message, client, *args, **kwargs):
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
        yield from client.send_message(message.channel, msg)
    else:
        if params[1] in base.functions:
            # check for docstring
            if base.functions[params[1]].__doc__:
                # Use inspect.getdoc() to clean the docstring up.
                yield from client.send_message(message.channel, inspect.getdoc(base.functions[params[1]]))
            else:
                yield from client.send_message(message.channel, ':heavy_exclamation_mark: This command has no docstring! Go tell Orangestar that it\'s broken.')
        else:
            yield from client.send_message(message.channel, ':no_entry_sign: That command does not exist.')

@base.cacofunc
def welcome(message, client, *args, **kwargs):
    '''
    **.welcome**
    Displays a helpful message about how to use CacoBot!
    *Example: `.welcome`*
    '''

    # You should customize this message to meet the standards of your own bot.

    yield from client.send_message(message.author, 'HISSSSSSS! I\'m **CacoBot** r20! I was made by **Orangestar** to help out with a Doom-related server, but now I roam Discord checking out the servers available. My purpose is to act as a *supplementary* bot to existing bots on your server. I\'m packing a bunch of weird, superfluous commands that keep me lightweight and don\'t obsolete other bots. You can check them out with the `.help` command! Some stuff you might be interested:\n\n`.quote`: Prints quotes that people have said in Discord servers! Feel free to add your own to the pile with `.addquote` if you come across someone saying something silly.\n\nUse `.log` to get a nice, copy-pastable copy of the last few messages in a channel to add to quotes or share with a friend.\n\nCheck out my Github repo and personal server with `.git`.\n\nI have a set of commands for saving hilarious quotes from other users! Log is perfect for adding quotes to this database. If you ever need a pick-me-up, call `.quote`!\n\nFor everything else, you should call .help  for a list of commands and .help [*command*] for specific information about a specific command. Have fun!')

# If you're taking the senic tour of the code, you're free to look around as you
# please from this point on, though I recommend checking out configs/config.json
