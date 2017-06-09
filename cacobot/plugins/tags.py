'''
Tags command
Allows users to store and recall strings of information.
'''

import json

import discord

from .. import Command
from .. import COLORS as colors
from .. import CacoBotException

class NonFatalError(CacoBotException): # pylint: disable=R0903
    '''
    Error that should be raised when cacobot should spew a non-fatal error at
    the user who caused it. Used for things like too few parameters.
    Pass the message to be sent as the exception's first parameter.
    '''
    def __init__(self, response):
        self.response = response

class Tags(Command):
    '''Tag command main class'''
    tags = {}
    tags_changed = False

    possible_commands = None

    def init(self, client):
        '''init command'''
        # Load tags JSON

        try:
            with open('./config/tags.json') as data:
                self.tags = json.load(data)

        # Create tags if not found
        except FileNotFoundError:
            with open('./config/tags.json', 'w') as data:
                data.write('{}')

        self.possible_commands = {
            'create' : {
                'aliases' : ('create', 'add', '+', 'make', 'new'),
                'method' : self.create_tag
            },
            'delete' : {
                'aliases' : ('delete', 'remove', '-'),
                'method' : self.delete_tag
            },
            'edit' : {
                'aliases' : ('edit', 'change', 'modify'),
                'method' : self.edit_tag
            },
            'rename' : {
                'aliases' : ('rename'),
                'method' : self.rename_tag
            },
            'help' : {
                'aliases' : ('help', '?'),
                'method' : self.tag_help
            }
        }

    async def tag_help(self, client, message, context):
        '''Provides help on using tags.'''
        embed = discord.Embed(
            title='Tag Help',
            description='The following commands are available for you to use. '
                        'Sample commands are provided for further understanding.',
            color=colors.default)

        embed.add_field(
            name='Create',
            value='`tag create "Richard Stallman" "AKA the GNU guy."`',
            inline=False)

        embed.add_field(
            name='Delete',
            value='`tag delete "My embarrassing high school vacation photos"`',
            inline=False)

        embed.add_field(
            name='edit',
            value='`tag edit "MST3K Night of the Blood Beast" "Hey Adam, the '
                  'link for this video died. Reup plox? -Jax"`',
            inline=False)

        embed.add_field(
            name='rename',
            value='`tag rename "Time of Your Life" "Good Riddance"`',
            inline=False)

        await client.send_message(message.channel, embed=embed)

    async def create_tag(self, client, message, context):
        '''Add a new tag to the tags database.'''
        try:
            # step 1: does this tag already exist
            if context[2] in self.tags:
                raise NonFatalError('A tag with that name already exists.')

            # step 2: are there too many parameters (meaning this dumbass didn't
            # shlex his args)
            if len(context) > 4:
                await client.send_message(message.channel, embed=discord.Embed(
                    title='Too Many Parameters',
                    color=colors.warning,
                    description='Condensing the last {} arguments into one. '\
                                'Please use command line-style arguments next '\
                                'time (i.e. '\
                                '`tag create justice "Free Hoxton"`)'.format(
                                    len(context) - 3)))

                context[3] = message.content.split(None, 3)[3]

            # now we get to make the tag
            self.tags[context[2]] = {
                'tag' : context[3],
                'owner' : message.author.id
            }
            # note to viewers: tag['server'] was deprecated.
            # Didn't work anyway.

            self.tags_changed = True

            await client.send_message(message.channel, embed=discord.Embed(
                title='Tag Created',
                color=colors.default,
                description=f'The tag "{context[2]}" has been added.'))

        except NonFatalError as error:
            await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='Error',
                    description=error.response,
                    color=colors.error))

    async def delete_tag(self, client, message, context):
        '''Remove a tag from the tag database'''
        try:
            # step 1: are there too many parameters (meaning this dumbass didn't
            # shlex his args)
            if len(context) > 3:
                await client.send_message(message.channel, embed=discord.Embed(
                    title='Too Many Parameters',
                    color=colors.warning,
                    description='Condensing the last {} arguments into one. '\
                                'Please use command line-style arguments next '\
                                'time (i.e. `tag delete "The Shins"`)'.format(
                                    len(context) - 2)))

                context[2] = message.content.split(None, 2)[2]

            # step 2: does this tag even exist
            if context[2] not in self.tags:
                raise NonFatalError('A tag with that name does not exist.')

            # step 3: does the invoker have permission to delete this tag
            if message.author.id != self.tags[context[2]]['owner']:
                raise NonFatalError('You do not own that tag, therefore you '
                                    'cannot modify it.')

            # axe it, jack
            self.tags.pop(context[2])
            self.tags_changed = True

            await client.send_message(message.channel, embed=discord.Embed(
                title='Tag Deleted',
                color=colors.default,
                description=f'Tag "{context[2]}" deleted.'))

        except NonFatalError as error:
            await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='Error',
                    description=error.response,
                    color=colors.error))

    async def edit_tag(self, client, message, context):
        '''Alter the contents of a tag.'''
        try:
            # step 1: does this tag even exist
            if context[2] not in self.tags:
                raise NonFatalError('A tag with that name does not exist.')

            # step 3: does the invoker have permission to edit this tag
            if message.author.id != self.tags[context[2]]['owner']:
                raise NonFatalError('You do not own that tag, therefore you '
                                    'cannot modify it.')

            # step 3: are there too many parameters (meaning this dumbass didn't
            # shlex his args)
            if len(context) > 4:
                await client.send_message(message.channel, embed=discord.Embed(
                    title='Too Many Parameters',
                    color=colors.warning,
                    description='Condensing the last {} arguments into one. '\
                                'Please use command line-style arguments next '\
                                'time (i.e. '\
                                '`tag edit jfa "Phoenix Wright did nothing '\
                                'wrong."`)'.format(len(context) - 3)))

                context[3] = message.content.split(None, 3)[3]

            self.tags[context[2]]['tag'] = context[3]
            self.tags_changed = True

            await client.send_message(message.channel, embed=discord.Embed(
                title='Tag Edited',
                color=colors.default,
                description=f'The contents of tag "{context[2]}" have changed.'))

        except NonFatalError as error:
            await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='Error',
                    description=error.response,
                    color=colors.error))

    async def rename_tag(self, client, message, context):
        '''Change the name of one tag to another'''
        try:
            # step 1: does this tag even exist
            if context[2] not in self.tags:
                raise NonFatalError('A tag with that name does not exist.')

            # step 3: does the invoker have permission to edit this tag
            if message.author.id != self.tags[context[2]]['owner']:
                raise NonFatalError('You do not own that tag, therefore you '
                                    'cannot modify it.')

            # step 3: are there too many parameters (meaning this dumbass didn't
            # shlex his args)
            if len(context) > 4:
                await client.send_message(message.channel, embed=discord.Embed(
                    title='Too Many Parameters',
                    color=colors.warning,
                    description='Condensing the last {} arguments into one. '\
                                'Please use command line-style arguments next '\
                                'time (i.e. '\
                                '`tag rename karmachameleon '\
                                '"Karma Chameleon"`)'.format(len(context) - 3)))

                context[3] = message.content.split(None, 3)[3]

            # step 4: is the other tag name already taken
            if context[3] in self.tags:
                raise NonFatalError('A tag with your newly-selected name already'
                                    ' exists.')

            self.tags[context[3]] = {
                'tag' : self.tags[context[2]]['tag'],
                'owner' : message.author.id
            }

            self.tags.pop(context[2])
            self.tags_changed = True

            await client.send_message(message.channel, embed=discord.Embed(
                title='Tag Renamed',
                color=colors.default,
                description=f'The tag "{context[2]}" has been renamed'
                            f'to "{context[3]}".'))

        except NonFatalError as error:
            await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='Error',
                    description=error.response,
                    color=colors.error))

    async def main(self, client, message, context):
        '''main function'''
        try:
            if len(context) < 2: # not enough parameters
                return await self.tag_help(client, message, context)

            for cmd in self.possible_commands:
                if context[1] in self.possible_commands[cmd]['aliases']:
                    # before we start: are there enough parameters for this command
                    if not cmd == 'help' and (\
                            (cmd == 'delete' and len(context) < 3) \
                            and len(context) < 4):
                        raise NonFatalError(f'Not enough parameters for `{cmd}`.')

                    return await self.possible_commands[cmd]['method'](
                        client,
                        message,
                        context)

            #if context[1] in ['create', 'delete', 'edit', 'rename']:
            #    raise NonFatalError('Tags are currently in read-only mode.')

            if len(context) > 2:
                # condense params for recall
                context[1] = message.content.split(maxsplit=1)[1]

            if context[1] not in self.tags:
                raise NonFatalError('Tag not found.')

            # send tag
            await client.send_message(
                message.channel,
                '\u2060' + self.tags[context[1]]['tag']
                )

        except NonFatalError as error:
            await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='Error',
                    description=error.response,
                    color=colors.error)
                )

    async def exit(self, client):
        '''bot close'''
        # unload tags
        if self.tags_changed:
            with open('./config/tags.json', 'w') as data:
                json.dump(self.tags, data)

    helpstring = 'Allows users to store and recall strings of text.'
    helpstring_smol = 'Storage and recall.'
    usage = '`tag create "quote example" "An example, using quotes"` to create '\
            'a tag.\n'\
            '`tag quote example` to recall a tag.\n'\
            'Other parameters supported: `delete`, `edit`, `rename`. Should be '\
            'self-explanatory. For more help, call `tag help`'
    aliases = ['tag', 't']

Tags()
