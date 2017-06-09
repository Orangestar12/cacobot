'''Main CacoBot interface: includes CacoBot class and Commands'''

import json # For handling configs
import shlex # splits message into bash-style chunks for easy processing
import sys, traceback # Handles error processing

from collections import namedtuple # more memory conservant than classe

import discord

Colors = namedtuple('Colors', 'default, error, warning') # This is called abuse, kids.
COLORS = Colors(
    default=discord.Color(0x882F2F),
    error=discord.Color(0xD52626),
    warning=discord.Color(0xFF8800)
    )

class CacoBotException(Exception):
    '''Exception specifically raised by CacoBot code.'''
    pass

class CommandParseException(CacoBotException):
    '''Raise when an added command is parsed and causes some kind of error.'''
    pass

class CacoBot(discord.Client):
    '''
    Main CacoBot class. Extend with the Command class instead. (automatically
    extends this class.)
    '''
    commands = set()
    config_modified = False

    def __init__(self, config):
        '''
        Initialize CB.
        "config" should be a string containing the location of a CB config file,
        in JSON. Refer to the CB sample config for more.
        '''
        with open(config) as data:
            self.config = json.load(data)

        self.invokers = self.config['invokers']
        self.app_info = None
        self.cfg_location = config

        for command in self.commands:
            command.init(self)

        super().__init__()

    async def on_ready(self):
        '''Run after successfully connecting to Discord.'''
        # we only, use app info to get the ID of the owner. this means we only
        # ever need to get it this once and never care about it again.
        self.app_info = await self.application_info()

        for command in self.commands:
            await command.ready(self)

        print('[Online]')

    async def on_message(self, message):
        '''Run after message is recieved'''
        if not message.content:
            # empty message (attachment, usually)
            return

        # TODO: early cacobot was made to collaborate with other bots in a
        #      friendly way. Think about bringing that back.
        if message.author.bot:
            return

        current_invoker = None

        for invoker in self.invokers:
            if message.content.lower().startswith(invoker):
                current_invoker = invoker
                break

        if current_invoker is None:
            return # no command

        try:
            context = shlex.split(message.content[len(current_invoker):])
        except ValueError:
            context = message.content[len(current_invoker):].split()

        if not context:
            # send fake error to owner if no context: This shouldn't ever happen.
            if message.channel.is_private:
                location_info = f'From private message with {message.author.name}:'
            else:
                location_info = f'Server: {message.server.name} | '\
                                  'Channel: {message.channel.name}\n'\
                                  'Authored by {message.author.name}.'

            return await self.send_message(
                self.app_info.owner,
                'Context somehow came back empty. Some measurements for '
                'debugging follow.\n'
                f'{location_info}\n'\
                f'{message.clean_content[:1900]}')

        for command in self.commands:
            if context[0].lower() in command.aliases:
                return await command.main(self, message, context)

    async def close(self):
        if self.is_closed:
            return # i'm sorry for all these hacks

        if self.config_modified:
            with open(self.cfg_location, 'w') as data:
                json.dump(self.config, data)

        for command in self.commands:
            await command.exit(self)

        await super().close()

    # Disable sending @everyones.
    async def send_message(self, destination, content=None, *, tts=False, embed=None):
        mentions = {'@everyone', '@here'}
        error_embed = discord.Embed(
            title='Fatal Error',
            description='DO NOT use this bot to circumvent everyone mention '\
                        'permission restrictions.',
            color=COLORS.error)

        if content:
            for ping in mentions:
                if ping in content:
                    return await self.send_message(
                        destination,
                        embed=error_embed)

        if embed:
            for ping in mentions:
                if embed.description and ping in embed.description:
                    return await self.send_message(
                        destination,
                        embed=error_embed)

                for field in embed.fields:
                    if ping in field.value:
                        return await self.send_message(
                            destination,
                            embed=error_embed)

        return await super().send_message(destination, content, tts=tts, embed=embed)

    async def on_error(self, event_method, *args, **kwargs):
        if args and isinstance(args[0], discord.Message):
            await self.send_message(
                args[0].channel,
                embed=discord.Embed(
                    title='Error',
                    description=sys.exc_info()[0].__name__,
                    color=COLORS.error)
                )

            error = traceback.format_exc()

            await self.send_message(
                self.app_info.owner,
                f'```{error}```')

    async def add_multiple_reactions(self, message, reactions):
        '''Add all reactions in "reactions" to message'''
        return_list = []
        for reaction in reactions:
            sent_reaction = await self.add_reaction(message, reaction)
            return_list.append(sent_reaction)

        return tuple(return_list)

class Command:
    '''
    Encapsulates possible cacobot commands. Replace the following:
    init (needs client): A method that is run when the bot starts up, but before
                         it connects to discord.
    ready (needs client): a method that is run when the bot connects to Discord.
    main (needs client, message, context): A method that actually gets run when
                                           you perform the command.
    settings (needs client, message, context): A method that gets run on the
                                               command "settings command".
                                               Optional.
    exit (needs client): A method that gets run when the bot closes. Optional.
    aliases: Either a set or list with aliases for your command.
    helpstring: Printed on "help command". Optional.
    helpstring_smol: Printed in the full command list, on "help". Optional.
    usage: An example of how the command should be used. Optional.
    '''
    def __init__(self):
        '''
        add command to possible cacobot commands
        DO NOT REPLACE, or at least call super().__init__()
        '''
        if 'main' not in dir(self): # This doesn't work but I tried
            raise CommandParseException(
                'A command must have a "main" method defined.'
                )
        CacoBot.commands.add(self)

    aliases = []

    def init(self, client):
        '''Initialization command, called when bot is started up.'''
        pass

    async def ready(self, client):
        '''Ready command, called after the bot connects.'''
        pass

    async def main(self, client, message, context):
        '''Main command, to be called when the command runs.'''
        pass

    async def exit(self, client):
        '''Close command, to be called when the bot exits.'''
        pass

    async def settings(self, client, message):
        '''
        Settings (OPTIONAL): This will be run when the command "settings
        command" is used. (command being one of the aliases in "aliases")
        '''
        return await client.send_message(
            message.channel,
            embed=discord.Embed(
                title='Error',
                description='This command has no alterable settings.',
                color=COLORS.error)
            )

    helpstring = 'This command has no set help string.'
    helpstring_smol = ''
    usage = ''

    # TODO: required_permission_level
    #       sets a permission (or, using ordered dicts, least required
    #       permission) that can run the command.

# defining some base, required commands.

class HelpCommand(Command):
    '''Provides help on existing commands'''
    async def main(self, client, message, context):
        '''main function'''
        if len(context) > 1:# asked for help on command
            # strip trailing ?
            if context[1].endswith('?'):
                context[1] = context[1][:-1]

            # strip leading invoker
            for invoker in client.invokers:
                if context[1].startswith(invoker):
                    context[1] = context[1][len(invoker):]

            for command in client.commands:
                if context[1] in command.aliases:
                    # found command, print helpstring
                    embed = discord.Embed(
                        title=command.aliases[0],
                        description=command.helpstring,
                        color=COLORS.default)

                    # display usage
                    if command.usage:
                        embed.add_field(
                            name='Example Use:',
                            value=command.usage,
                            inline=False)

                    # display aliases
                    if len(command.aliases) > 1:
                        embed.add_field(
                            name='Aliases:',
                            value=', '.join(command.aliases[1:]),
                            inline=False)

                    # send message
                    return await client.send_message(
                        message.channel,
                        embed=embed)

                # end found command
            # command not found
            return await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='Not Found',
                    description='A command with that name was not found.',
                    color=COLORS.error)
                )

        # print all commands
        helpmsg = discord.Embed(
            title='Available Commands:',
            color=COLORS.default)

        for command in client.commands:
            if command.helpstring_smol:
                helpmsg.add_field(
                    name=command.aliases[0],
                    value=command.helpstring_smol)

        await client.send_message(
            message.channel,
            embed=helpmsg)

    aliases = [
        'help',
        'whats',
        'what\'s'
    ]
    helpstring = 'Provides help on existing commands.\n' \
                'Provide a command to get longer, more detailed information ' \
                'on that specific command.'
    helpstring_smol = 'Get help on commands.'
    usage = '`help`: List all commands.\n' \
            '`help quote`: Get help on "quote" command.'

HelpCommand()

class OptionsCmd(Command):
    '''configure settings for commands'''
    async def main(self, client, message, context):
        '''the function itself'''
        if len(context) < 2: # no command specified
            return await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='No Command Specified',
                    description='This command is to be used with another '\
                                'command\'s name as a parameter. See `help '\
                                'settings` for more information.',
                    color=COLORS.error)
                )

        # strip leading invoker
        for invoker in client.invokers:
            if context[1].startswith(invoker):
                context[1] = context[1][len(invoker):]

        for command in client.commands:
            if context[1] in command.aliases:
                # found command, run settings for it
                return await command.settings(client, message)

        # command not found
        return await client.send_message(
            message.channel,
            embed=discord.Embed(
                title='Not Found',
                description='A command with that name was not found.',
                color=COLORS.error)
            )

    aliases = [
        'settings',
        'options',
        'change'
    ]
    helpstring = 'Allows server owners to change how some commands work when '\
                 'used on their server, and allows users to customize how '\
                 'some commands work for them personally. This is dependent on '\
                 'the command.'
    helpstring_smol = 'Customize commands.'
    usage = '`settings command`: Adjust settings for the command "command".'

OptionsCmd()

class Debug(Command):
    '''admin-only debug command'''
    async def main(self, client, message, context):
        '''main Debug func'''
        # don't continue if not bot owner
        if message.author != client.app_info.owner:
            return
        if len(context) > 2 and context[1] == 'await':
            response = await eval(message.content.split(None, 2)[2]) # pylint: disable=W0123
            return await client.send_message(message.channel, str(response))

        return await client.send_message(
            message.channel,
            str(eval(message.content.split(None, 1)[1]))) # pylint: disable=W0123

    aliases = [
        'debug',
        'do'
    ]

Debug()
