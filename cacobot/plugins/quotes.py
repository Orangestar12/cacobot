'''
Quotes commands
Allows users to submit and recall humorous quotes from other users.
'''

import json
import random
import os

import discord

from .. import Command
from .. import COLORS as colors
from .. import CacoBotException

class CommandTimeoutException(CacoBotException):
    '''
    Raised when wait_for_message times out.
    '''
    pass

class CommandCancelledException(CacoBotException):
    '''
    Raised when the content is "cancel".
    '''
    pass

class NonFatalError(CacoBotException): # pylint: disable=R0903
    '''
    Error that should be raised when cacobot should spew a non-fatal error at
    the user who caused it. Used for things like too few parameters.
    Pass the message to be sent as the exception's first parameter.
    '''
    def __init__(self, response):
        self.response = response

class MainQuotesCommand(Command):
    '''main ".quotes" command, for recalling quotes'''
    configs = {
        'quotes' : {},
        'user_settings' : [],
        'server_settings': []
    }

    changed_jsons = set()

    def init(self, client):
        '''init quotes'''
        # make new quotes folder in configs if none
        os.makedirs('./config/quotes', exist_ok=True)

        # Load quotes and user data
        for filename, item in [
                ('./config/quotes/quotes.json', 'quotes'),
                ('./config/quotes/quote_user_prefs.json', 'user_settings'),
                ('./config/quotes/quote_server_prefs.json', 'server_settings')
        ]:
            try:
                # open the file
                with open(filename) as file:
                    self.configs[item] = json.load(file)

            except FileNotFoundError:
                # file doesn't exist, make it
                with open(filename, 'w') as newfile:
                    if filename == 'quotes':
                        newfile.write('{}')
                    else:
                        newfile.write('[]')

    async def retrieve_quote(self, index=0, off=False, string=None):
        '''
        Get a quote by index or string. Returns a tuple: (quote index, quote)
        '''

        if (index <= 0 and not string) or index > len(self.configs['quotes']):
            raise NonFatalError('You must specify a number between 1 and '
                                f'{len(self.configs["quotes"])}.')

        if not string:
            if off and self.configs['quotes'][index-1]['o']:
                raise NonFatalError('This quote has been flagged as '
                                    f'potentially offensive, and this {off} is '
                                    'set to not recieve such quotes.')

            quote = self.configs['quotes'][index-1]['quote']
            quotenum = index
        else:
            tally = False

            if string.startswith('tally='):
                tally = True
                string = string[6:]
            elif string.startswith('search='):
                string = string[7:]

            if not string:
                raise NonFatalError('You must provide a string to search '
                                    'for when using a named argument. '
                                    '(Example: `search=Miami Mutilator`)')

            # go searching for the string
            possible_quotes = [i for i, x in enumerate(self.configs['quotes']) if \
                                  string in x['quote'] and x['o'] == bool(off)]

            # TODO: make this use regex word boundaries

            if tally:
                return (f'list for "{string}"', ' '.join((str(x+1) for x in possible_quotes)))

            if not possible_quotes:
                raise NonFatalError('No quotes were found with the specified '
                                    'string.')

            if len(possible_quotes) == 1:
                # one quote found with that string in it
                quote = self.configs['quotes'][possible_quotes[0]]['quote']
                quotenum = possible_quotes[0] + 1

            else:
                # get random quote from possible_choices
                this_quote = random.choice(possible_quotes)
                quote = self.configs['quotes'][this_quote]['quote']
                quotenum = this_quote + 1

        return (quotenum, quote)


    async def main(self, client, message, context):
        '''main command'''

        # check to see if the user has opted out of o-flagged quotes
        off = False # short for **off**ensive

        if not message.channel.is_private and \
                message.server.id in self.configs['server_settings']:
            # server has o-quotes disabled
            off = 'server'

        elif message.author.id in self.configs['user_settings']:
            # user has o-quotes disabled
            off = 'user'

        try:
            # no specification: random quote
            if len(context) == 1:
                while True:
                    pos_quote = random.randint(1, len(self.configs['quotes']))

                    if not off or not self.configs['quotes'][pos_quote-1]['o']:
                        break

                quote = await self.retrieve_quote(pos_quote, off)
            else:
                try:
                    # get quote by index
                    quote = await self.retrieve_quote(int(context[1]), off)
                except ValueError:
                    # get quote by search
                    quote = await self.retrieve_quote(off=off, string=message.content.split(maxsplit=1)[1])

        except NonFatalError as error:
            await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='Error',
                    description=error.response,
                    color=colors.error)
                )

        else:
            quote_embed = discord.Embed(
                title=f"Quote number {quote[0]}",
                description=quote[1],
                color=colors.default
            )

            if off:
                quote_embed.set_footer(
                    text=f'Offensive quotes are disabled for this {off}.'
                )

            await client.send_message(
                message.channel,
                embed=quote_embed)

    async def set_personal_settings(self, client, message):
        '''opt in or out of offensive quotes personally.'''
        notice = 'Before we continue, please consider this excerpt from '\
                 'the `man` page for the BSD `fortune` command:\n'\
                 '```Please,  please,  please request...potentially offensive '\
                 'fortune[s] if and only if you believe, deep in your heart, '\
                 'that you are willing to be offended. (And that you\'ll just '\
                 'quit using [them] rather than give us grief about it, okay?)\n'\
                 '\n'\
                 '... let us keep in mind the basic governing philosophy of The '\
                 'Brotherhood, as handsomely summarized in these words: we '\
                 'believe in healthy, hearty laughter -- at the expense of the '\
                 'whole human race, if needs be.  Needs be.\n'\
                 '    --H. Allen Smith, "Rude Jokes"```\n'\
                 '\n'\
                 'To confirm, please react with \U0001F197.'

        if message.author.id in self.configs['user_settings']:
            title = 'You are about to opt into receiving '\
                    'potentially offensive quotes.'
        else:
            title = 'You are about to opt out of receiving '\
                    'potentially offensive quotes.'

        msg = await client.send_message(
            message.author,
            embed=discord.Embed(
                title=title,
                description=notice,
                color=colors.warning)
            )

        emojis = [
            '\U0001F197', # OK button
            '\u274c' # negative squared cross mark
        ]

        await client.add_multiple_reactions(
            msg,
            emojis)

        reaction = await client.wait_for_reaction(
            emojis,
            message=msg,
            user=message.author,
            timeout=60)

        if not reaction:
            raise CommandTimeoutException

        if reaction.reaction.emoji == emojis[1]:
            raise CommandCancelledException

        if message.author.id in self.configs['user_settings']:
            self.configs['user_settings'].remove(message.author.id)
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Opted-in',
                    description='You have opted into receiving all quotes.',
                    color=colors.default)
                )
        else:
            self.configs['user_settings'].append(message.author.id)
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Opted-out',
                    description='You have opted out of recieving '\
                                'potentially offensive quotes.\n\n'\
                                '**Please keep in mind this does not disable '\
                                'the ability for other people to call these '\
                                'quotes.**',
                    color=colors.warning)
                )

        self.changed_jsons.add('user_settings')

    async def set_serverwide_settings(self, client, message):
        '''opt in or out of offensive quotes across a whole server.'''
        await client.send_message(
            message.author,
            embed=discord.Embed(
                title='Enter Server Title',
                description='Please enter the name of the server you would like'\
                            ' to toggle potentially offensive quotes on.\n\n'\
                            '(This is symbol-strict, but not case sensitive. '\
                            '"Pin-Bot\'s Place" and "pin-bot\'s place" would '
                            'both return the same server.)',
                color=colors.warning)
            )

        server_name = await client.wait_for_message(
            author=message.author,
            check=lambda x: x.channel.is_private,
            timeout=60)

        if not server_name:
            raise CommandTimeoutException

        server = discord.utils.find(
            lambda x: x.name.lower() == server_name.content.lower(),
            client.servers)

        if not server:
            raise NonFatalError('Server not found. Are you sure you typed the '
                                'name correctly?')

        possible_mod = server.get_member(message.author.id)

        if not possible_mod:
            raise NonFatalError('Couldn\'t find you among the users in that '
                                'server.\n\nRarely, this is due to sharding, '
                                'so if you\'re sure you typed the right server, '
                                'just try again in a moment. (Sending a quick '
                                'message in the server helps!)')

        if not server.default_channel.permissions_for(possible_mod).administrator:
            raise NonFatalError('You do not have the "Administrator" permission on '
                                'that server.')

        description = '{}\n\nTo confirm, please react with \U0001F197.'
        title = f'Toggling Quote Settings for {server.name}'

        if server.id in self.configs['server_settings']:
            description.format('You are about to remove the restriction on '
                               f'potentially offensive quotes in {server.name}.')
        else:
            description.format('You are about to disable the ability for all '
                               f'users in {server.name} to call potentially '
                               'offensive quotes.')

        msg = await client.send_message(
            message.author,
            embed=discord.Embed(
                title=title,
                description=description,
                color=colors.warning)
            )

        emojis = [
            '\U0001F197', # OK button
            '\u274c' # negative squared cross mark
        ]

        await client.add_multiple_reactions(
            msg,
            emojis)

        reaction = await client.wait_for_reaction(
            emojis,
            message=msg,
            user=message.author,
            timeout=60)

        if not reaction:
            raise CommandTimeoutException

        if reaction.reaction.emoji == emojis[1]:
            raise CommandCancelledException

        if server.id in self.configs['server_settings']:
            self.configs['server_settings'].remove(server.id)
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Opted-in',
                    description=f'Users in {server.name} can now call any quote.',
                    color=colors.default)
                )
        else:
            self.configs['server_settings'].append(server.id)
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Opted-out',
                    description=f'Users in {server.name} can no longer call '\
                                'potentially offensive quotes.',
                    color=colors.default)
                )

        self.changed_jsons.add('server_settings')

    async def settings(self, client, message):
        '''settings for quotes'''
        if not message.channel.is_private:
            await client.send_message(
                message.channel,
                embed=discord.Embed(
                    title='Continued in DMs',
                    description='This command will continue in your DMs.',
                    color=colors.default)
                )

        thing_to_say = 'Some quotes could potentially be seen as "Offensive". '\
                       'By default, the `quote` command will call quotes '\
                       'indiscriminately of whether they are flagged as '\
                       'potentially offensive or not. You can disable this '\
                       'for all quotes you send, or for all users calling the '\
                       'command in a server where you have the "Administrator" '\
                       'permission.\n\n'

        emojis = [
            '\U0001F464', # bust in silhouette
            '\U0001F465', # busts in silhouette
            '\u274c' # negative squared cross mark
        ]

        if message.author.id in self.configs['user_settings']:
            thing_to_say += 'You are currently personally set to '\
                            '***avoid*** receiving potentially offensive '\
                            'quotes.'
        else:
            thing_to_say += 'You are currently personally set to receive '\
                            'all quotes, regardless of their potential '\
                            'offensiveness. This is the default.'

        thing_to_say += '\n\n\U0001F464: Toggle personal opt-out\n'\
                       '\U0001F465: Toggle serverwide opt-out\n'\
                       '\u274c: Close settings.'

        try:
            msg = await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Settings for the "quote" command',
                    description=thing_to_say,
                    color=colors.default)
                )

            await client.add_multiple_reactions(
                msg,
                emojis)

            reaction = await client.wait_for_reaction(
                emojis,
                message=msg,
                user=message.author,
                timeout=60)

            if not reaction:
                raise CommandTimeoutException

            if reaction.reaction.emoji == emojis[0]:
                return await self.set_personal_settings(client, message)
            if reaction.reaction.emoji == emojis[1]:
                return await self.set_serverwide_settings(client, message)

            raise CommandCancelledException

        except CommandTimeoutException:
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Time Out',
                    description='Request timed out.',
                    color=colors.error)
                )
        except CommandCancelledException:
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Cancelled',
                    description='Request cancelled. Thank you for your time.',
                    color=colors.error)
                )
        except NonFatalError as error:
            await client.send_message(
                message.author,
                embed=discord.Embed(
                    title='Error',
                    description=error.response,
                    color=colors.error)
                )

    async def exit(self, client):
        '''bot close'''

        for filename, item in [
                ('./config/quotes/quotes.json', 'quotes'),
                ('./config/quotes/quote_user_prefs.json', 'user_settings'),
                ('./config/quotes/quote_server_prefs.json', 'server_settings')
        ]:
            if item in self.changed_jsons:
                with open(filename, 'w') as data:
                    json.dump(self.configs[item], data)

    helpstring = 'Recalls a directed, specific, or random quote.\n'\
                 '*This command is part of the "Quotes Suite"*'
    helpstring_smol = 'Recall humorous quotes'
    usage = '`quote 5` to recall the 5th quote.\n'\
            '`quote` to get a random quote.\n'\
            '`quote this jelly` to recall a random quote with the string "this'\
            ' jelly" in it.\n'\
            '`quote search=500`; preceding your command with "search=" will '\
            'force a search with the given phrase, allowing you to search for '\
            'integers in quotes.\n'\
            '`quote tally=kitchen ace` to get a list of all quote IDs with '\
            '"kitchen ace" in them'
    aliases = ['quote', 'quotes', 'q']

MainQuotesCommand()
