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

        msg += 'Use `.help [`*`command`*`]` to get more information about a command.\nUse `.help all` to get a verbose image listing CacoBot\'s functions.'
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

# If you're taking the senic tour of the code, you're free to look around as you
# please from this point on, though I recommend checking out configs/config.json
