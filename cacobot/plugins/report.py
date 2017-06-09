'''
Report command
Allows users to send messages descreetly to the staff of the server.
'''

import json
import discord

from .. import Command
from .. import COLORS as colors

from .. import CacoBotException

class CommandTimeoutException(CacoBotException):
    '''
    Raised by message_waiter when wait_for_message times out.
    '''
    pass

class CommandCancelledException(CacoBotException):
    '''
    Raised by message_waiter when the content is "cancel".
    Can be raised elsewhere to "Skip" to the cancel exception resolution.
    '''
    pass

class MessageAlreadySentException(CacoBotException):
    '''
    Raised when some command that may return an error does so.
    '''
    pass

class Report(Command):
    '''Report command main class'''
    reports = {}
    reports_changed = False

    def init(self, client):
        '''init command'''
        # Load reports channels for servers
        try:
            with open('./config/reports.json') as data:
                self.reports = json.load(data)

        # Create tags if not found
        except FileNotFoundError:
            with open('./config/reports.json', 'w') as data:
                data.write('{}')

    async def timeout(self, client, channel):
        '''Inform the user on "channel" that their message wait timed out.'''
        return await client.send_message(
            channel,
            embed=discord.Embed(
                title='Time out',
                description='Request timed out.',
                color=colors.error)
            )

    async def reaction_waiter(
            self, client, emoji=None, *, user=None, timeout=60, message=None, check=None):
        '''
        Callse client.wait_for_reaction and automatically raises a timeout error
        if time expires, and a cancel error if emoji is u274c.
        The timeout is 60 by default.
        '''
        if '\u274c' not in emoji:
            emoji.append('\u274c')

        reacted = await client.wait_for_reaction(
            emoji=emoji,
            user=user,
            timeout=timeout,
            message=message,
            check=check)

        if reacted is None:
            raise CommandTimeoutException

        if reacted.reaction.emoji == '\u274c':
            raise CommandCancelledException

    async def message_waiter(
            self, client, timeout=60, *, author=None, channel=None, content=None, check=None):
        '''
        Calls client.wait_for_message, and automatically raises a timeout error
        if time expires, and a cancel error if content is cancel.
        The timeout is 60 by default.
        '''
        resolution = await client.wait_for_message(
            timeout=timeout,
            author=author,
            channel=channel,
            content=content,
            check=check)

        if resolution is None:
            raise CommandTimeoutException

        if resolution.content.lower() == 'cancel':
            raise CommandCancelledException

        return resolution

    async def dm_server_discerner(self, client, message, possible_servers):
        '''discern which server a dming user is attempting to report to'''
        if len(possible_servers) == 1:
            # user's only in one reportable server (neato!)
            return possible_servers[0]

        # multiple servers found
        desc = 'Multiple servers found. Which were you targeting?'

        # do not provide list of servers if there are too many
        if len(possible_servers) > 9:
            desc += f' ({len(possible_servers)} servers are available.)'
        else:
            desc += '\n\n__**Possible Servers:**__\n{}'.format(
                "\n".join((x.name for x in possible_servers))
                )

        await client.send_message(
            message.channel,
            embed=discord.Embed(
                title='Warning',
                description=desc,
                color=colors.default)
            )

        msg = await self.message_waiter(
            client,
            channel=message.channel)

        # reevaluate possible servers
        possible_servers = [x for x in possible_servers if \
            x.name.lower() == msg.content.lower()]

        # no servers with that name
        if not possible_servers:
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Error',
                    description='No servers found. Make sure you typed'\
                                ' in the name correctly and that the '\
                                'server in question has a report '\
                                'channel set up.',
                    color=colors.error)
                )
            raise MessageAlreadySentException

        if len(possible_servers) == 1:
            # server get
            return possible_servers[0]

        # multiple servers with the same name (HOLY SHIT DUDE)
        sent = await client.send_message(
            message.channel,
            embed=discord.Embed(
                title='Multiple Servers Found',
                description='There are several servers with that name. Which '\
                            'did you mean?\n\n{}'.format(
                                '\n'.join(
                                    (f'{i+1}. {x.name}' for i, x in \
                                        enumerate(possible_servers))
                                    )
                                ),
                color=colors.default)
            )

        if len(possible_servers) < 9:
            # reaction mode
            emojis = [f'{x}\u20e3' for x in range(1, len(possible_servers)+1)]
            emojis.append('\u274c')

            await client.add_multiple_reactions(sent, emojis)

            # old way
            #for num in range(1, len(possible_servers)+1):
            #    await client.add_reaction(sent, f'{num}\u20e3')

            react = await self.reaction_waiter(
                client,
                emojis,
                message=sent)

            return possible_servers[int(react.reaction.emoji[0]) - 1]

        # numerics mode
        msg = await self.message_waiter(
            client,
            check=lambda x: x.content.lower() == 'cancel' or \
                            int(x.content) <= len(possible_servers),
            channel=message.channel)

        # ValueErrors get auto-reported with on_error.
        return possible_servers[int(msg.content) - 1]

    async def main(self, client, message, context):
        '''main function'''
        try:
            server = None

            if message.channel.is_private:
                possible_servers = [x for x in client.servers if \
                    x.id in self.reports and \
                    message.author in x.members]

                # no reportable servers
                if not possible_servers:
                    await client.send_message(
                        message.author,
                        embed=discord.Embed(
                            title='Error',
                            description='You are not in any servers that have a '\
                                        'report channel set up. Please ask your '\
                                        'server administration for help.',
                            color=colors.error)
                        )
                    raise MessageAlreadySentException

                server = self.dm_server_discerner(client, message, possible_servers)

            else: # public
                # delete message for anonymity
                if not message.channel.permissions_for(
                        message.server.me).manage_messages:
                    # can't delete messages
                    await client.send_message(
                        message.channel,
                        embed=discord.Embed(
                            title='Warning',
                            description='I cannot delete messages in this server. '\
                                        'Your anonymity is not guaranteed.',
                            color=colors.warning)
                        )
                else:
                    await client.delete_message(message)

                server = message.server

            if len(context) < 1:
                await client.send_message(
                    message.author,
                    embed=discord.Embed(
                        title='Awaiting Report...',
                        description='Please send the text you would like to '\
                                    f'anonymously report to "{server.name}".',
                        color=colors.default)
                    )
                response = await self.message_waiter(
                    client,
                    check=lambda x: x.channel.is_private,
                    author=message.author)

                report_content = response.content
            else:
                report_content = message.content.split(maxsplit=1)[1]

            if server.id not in self.reports:
                await client.send_message(
                    message.author,
                    embed=discord.Embed(
                        title='Error',
                        description='The specified server does not have a report '\
                                    'channel set. Please contact an administrator.',
                        color=colors.error)
                    )
                raise MessageAlreadySentException

            constructed_embed = discord.Embed(
                color=colors.error,
                title='A report has been recieved.',
                description=report_content)

            await client.send_message(
                server.get_channel(self.reports[server.id]),
                embed=constructed_embed)

            sent = await client.send_message(
                message.author,
                embed=discord.Embed(
                    color=colors.warning,
                    title='Success',
                    description='Your report has been recieved. Would you like'\
                                  ' a copy of the report, exactly how it appears'\
                                  ' to the staff, for your records? (Use reactions.)')
                )

            emojis = [
                '\u2705', # heavy check
                '\u274c' # negative squared cross mark
            ]

            await client.add_multiple_reactions(
                sent,
                emojis)

            try:
                # Spaghetti'd so hard I don't have to return *or* check this value.
                await self.reaction_waiter(
                    client,
                    emojis,
                    message=sent)

                await client.send_message(
                    message.author,
                    embed=constructed_embed)

            except CommandCancelledException:
                await client.send_message(
                    message.author,
                    embed=discord.Embed(
                        color=colors.default,
                        description='Ok. Thank you for your time.')
                    )

        except CommandTimeoutException:
            return await self.timeout(client, message.author)

        except CommandCancelledException:
            return await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Error',
                    description='Request cancelled. Have a good day.',
                    color=colors.error)
                )

        except MessageAlreadySentException:
            pass

    async def remove_report_channel(self, client, message, server):
        '''Remove a report channel from the list.'''
        self.reports.pop(server.id)
        self.reports_changed = True

        return await client.send_message(
            message.author,
            embed=discord.Embed(
                title=f'Removing report channel on {server.name}',
                description='Successfully disabled reports for '\
                            f'{server.name}. If this was a mistake, you '\
                            'can reenable it through `settings report` just'\
                            ' as before.',
                color=colors.default)
            )

    async def set_report_channel(self, client, message, server):
        '''Add or update the report channel for a server.'''

        await client.send_message(
            message.author,
            embed=discord.Embed(
                title=f'Setting report channel on {server.name}',
                description='Please enter the name of the channel on your '\
                            'server that you would like reports to be sent '\
                            'to.',
                color=colors.default)
            )

        msg = await self.message_waiter(
            client,
            check=lambda x: x.channel.is_private,
            author=message.author)

        channel = discord.utils.find(
            lambda x: x.type == discord.ChannelType.text and \
                      x.name.lower() == msg.content.lower(),
            server.channels)

        if channel is None:
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Channel not found.',
                    description=f'Couldn\'t find a channel in {server.name}'\
                                ' with that name. Are you sure you spelled'\
                                ' it correctly?',
                    color=colors.error)
                )
            raise MessageAlreadySentException

        self.reports[server.id] = channel.id
        self.reports_changed = True

        return await client.send_message(
            message.author,
            embed=discord.Embed(
                title=f'Report channel for {server.name} set',
                description=f'Successfully set <#{channel.id}> as the '\
                            'report channel for your server. Users can now '\
                            'use `report` to send messages to your staff '\
                            'anonymously. I will send them to your specified'\
                            ' channel.\n\n\U0001F44D', # :thumbsup:
                color=colors.default)
            )

    async def settings(self, client, message):
        '''settings method'''
        server = None

        try:
            if message.channel.is_private:
                # dm: ask which server
                possible_servers = [server for server in client.servers if \
                                    discord.utils.find(
                                        lambda m: m.id == message.author.id,
                                        server.members) and \
                                    server.default_channel.permissions_for(
                                        server.get_member(message.author.id)
                                    ).manage_channels]

                if not possible_servers:
                    await client.send_message(
                        message.channel,
                        embed=discord.Embed(
                            title='No Servers Found',
                            description='You do not manage channels in any servers '\
                                        'I am in.',
                            color=colors.error)
                        )
                    raise MessageAlreadySentException

                server = self.dm_server_discerner(client, message, possible_servers)

            else:
                # public - set server, continue in dms
                if not message.channel.permissions_for(message.author).manage_channels:
                    await client.send_message(
                        message.channel,
                        embed=discord.Embed(
                            title='Insufficient Permissions',
                            description='You do not have permission to manage '\
                                        'channels in this server.',
                            color=colors.error)
                        )
                    raise MessageAlreadySentException

                server = message.server
                await client.send_message(
                    message.channel,
                    embed=discord.Embed(
                        title='Continued in DMs.',
                        description='This command will continue in your dms.',
                        color=colors.warning)
                    )

            # server is determined. Let's go:

            if server.id in self.reports:
                sent = await client.send_message(
                    message.author,
                    embed=discord.Embed(
                        title=f'"report" Settings for {server.name}',
                        description='*Your report channel is set to '\
                                    f'<#{self.reports[server.id]}>. Here\'s what you '\
                                    'can do:*\n'\
                                    '1\u20e3. Set report channel.\n'\
                                    '2\u20e3. Turn off report channel.\n'\
                                    '*React using the proper number.'\
                                    ' React with \u274c to quit.*',
                        color=colors.default)
                    )

                reactions = ['1\u20e3', '2\u20e3', '\u274c']

            else:
                sent = await client.send_message(
                    message.author,
                    embed=discord.Embed(
                        title=f'"report" Settings for {server.name}',
                        description='*Your have no set report channel. '\
                                    'Here\'s what you can do:*\n'\
                                    '1\u20e3. Add report channel.\n'\
                                    '*React using the proper number.'\
                                    ' React with \u274c to quit.*',
                        color=colors.default)
                    )

                reactions = ['1\u20e3', '\u274c']

            await client.add_multiple_reactions(
                sent,
                reactions)

            react = await self.reaction_waiter(
                client,
                reactions,
                message=sent)

            responses = {
                '2\u20e3' : self.remove_report_channel,
                '1\u20e3' : self.set_report_channel
            }

            responses[react.reaction.emoji](client, message, server)

        except CommandTimeoutException:
            return await self.timeout(client, message.author)

        except CommandCancelledException:
            return await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Error',
                    description='Request cancelled. Have a good day.',
                    color=colors.error)
                )

        except MessageAlreadySentException:
            pass

    async def exit(self, client):
        '''bot close'''
        # Load reports channels for servers
        if self.reports_changed:
            with open('./configs/reports.json') as data:
                json.dump(self.reports, data)

    helpstring = 'Allows users to send messages discreetly to the staff of a '\
                 'server.'
    helpstring_smol = 'Report to staff.'
    usage = '`report This green armored guy keeps DMing me photos of rockets.`\n'\
            'This command is not shlexed. Provide at max 1900 words detailing '\
            'your report.'
    aliases = ['report']

#init
Report()
