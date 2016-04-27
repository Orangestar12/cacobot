import json # for config and quotes.json loading
import random # for random quote numbers
import re # for syntax matching
import asyncio # to sleep in log

import discord
import cacobot.base as base

mention_syntax = re.compile(r'(<@([0-9#]*?)>)')

@base.cacofunc
async def quote(message, client):
    '''
    **{0}quote** [ *id* | *phrase to search* ]
    Spews a random quote from my database. If *id* is provided, spews the quote with that id. If *phrase to search* is provided, searches my database for quotes containing that phrase, lists every quote with that phrase, and then spews a random one from that list.
    *Example: `{0}quote 1`*
    '''
    numburs = ['number ', 'numero ', 'numbuh ', '#', 'integer ', '№ ']
    search = False
    r = 0

    try:
        with open('configs/quotes.json') as qdata:
            quotes = json.load(qdata)
    except FileNotFoundError:
        await client.send_message(message.channel, 'I do not have any quotes to puke.')
        return

    if len(message.content.strip().split()) > 1:
        try:
            r = int(message.content.split()[1])
        except ValueError:
            if re.match(r'^[0-9]*\.[0-9]*$', message.content.split(None, 1)[1]):
                await client.send_message(
                    message.channel,
                    '2:23 AM - 🎮 Mr McPowned: @KeksGiven to be fair, he can\'t store floats\n2:23 AM - 🎮 Mr McPowned: And if he did, I\'d call him retarded'
                    )
                return

            search = True

            msgslist = [i for i, x in enumerate(quotes) if message.content.split(None, 1)[1].lower() in x[0].lower()]

            if not msgslist:
                await client.send_message(
                    message.channel,
                    'I did not find any quotes with "{}" in them.'.format(
                        message.content.split(None, 1)[1].lower()
                        )
                    )
                return

            r = random.choice(msgslist) + 1

    if search:
        msg = '**The following quotes matched your query**:\n'
        for x in msgslist:
            msg += '{} '.format(x+1)
        msg = msg[:-1]
        msg += '\n*This is quote {}{} from your query*:\n{}'.format(
            random.choice(numburs),
            r, quotes[r-1][0]
            )
        await client.send_message(message.channel, msg)
        return

    if r == 0:
        qindex = random.randint(0, len(quotes))
        await client.send_message(
            message.channel, '*This is quote {}{}:*\n{}'.format(
                random.choice(numburs),
                qindex,
                quotes[qindex-1][0]
                )
            )
    elif r < 1:
        await client.send_message(
            message.channel,
            'You probably think you\'re really clever. Specify a *positive* quote index next time. Better yet: specify none at all for a random quote.'
            )
    elif r > len(quotes):
        await client.send_message(
            message.channel,
            ':no_entry_sign: You have specified a quote index that is too high. I only have {} quotes to puke.'.format(
                len(quotes)
            )
        )
    else:
        await client.send_message(message.channel, quotes[r-1][0])
quote.server = 'Quotes'

@base.cacofunc
async def addquote(message, client):
    '''
    **addquote** <*content*>
    Add a quote to my quote database.
    *Remember, quotes are subject to the Terms of Service for CacoBot, and my judgement. I do go through them. Shitty quotes that make no sense in any context, or quotes that try to be "meta" and refer to the quote index, are often subjected to deletion.*
    *Example: `{0}addquote <TerminusEst13> .idgames good map
    <idgamesbot> Nothing found.
    <TerminusEst13> Well there you have it, folks.`*
    '''
    cmd = message.content.split(None, 1)[1].strip()

    # Complain about cheeky asses.

    if cmd.startswith(base.config['invoker'] + 'addquote'):
        await client.send_message(
            message.channel,
            '{}: Hah hah, very funny, but that wouldn\'t work anyway.'.format(message.author)
            )

    elif cmd.startswith(base.config['invoker'] + 'quote'):
        await client.send_message(
            message.channel,
            '{}: Not only would that not work, but that\'s really annoying. Stop that shit.'.format(message.author)
            )

    else: # Actually add a quote

        # open quotes file. Make file if it doesn't exist
        quotes = []
        try:
            with open('configs/quotes.json') as z:
                quotes = json.load(z)
        except FileNotFoundError:
            with open('configs/quotes.json', 'w') as z:
                z.write('[]')

        if not [x[0] for x in quotes if x[0] == cmd]:
            # Add quote to list
            #replace mentions
            while mention_syntax.search(cmd):
                member = discord.utils.get(
                    message.server.members,
                    id=mention_syntax.search(cmd).group(2)
                    )

                if member:
                    cmd = cmd.replace(
                        mention_syntax.search(cmd).group(1),
                        '@' + member.name)
                else:
                    cmd = cmd.replace(
                        mention_syntax.search(cmd).group(1),
                        '@invalid_user'
                    )

            cmd = cmd.replace('@everyone', '@\u2020everyone').replace('@here', '@\u2020here')

            quotes.append([cmd, message.author.id])

            # Save file.
            with open('configs/quotes.json', 'w') as z:
                json.dump(quotes, z, indent=4)

            if cmd.startswith('http://') or cmd.startswith('https://'):
                await client.send_message(
                    message.channel,
                    '{}: :warning: I have added that quote successfully as number {}, but couldn\'t help noticing it starts with a link. If this is an image of a Discord chat log, consider providing your quotes as text next time, or using my `{}log` function.'.format(
                        message.author.name,
                        len(quotes),
                        base.config['invoker']
                        )
                    )
            else:
                await client.send_message(
                    message.channel,
                    '{}: :heavy_check_mark: Successfully added that to my quote database as quote number {}.'.format(
                        message.author.name,
                        len(quotes)
                        )
                    )
        else:
            await client.send_message(
                message.channel,
                '{}: :no_entry_sign: I already have that exact quote in my database.'.format(message.author))
addquote.server = 'Quotes'

@base.cacofunc
async def delquote(message, client):
    '''
    **{0}delquote** [*index*]
    Removes a quote from the database. You can only remove quotes you have created. Specify no index to try to remove the last quote.
    *Example: `{0}delquote 13`*
    '''

    cont = True

    if len(message.content.split()) != 1:
        try:
            r = int(message.content.split()[1])
        except ValueError:
            await client.send_message(
                message.channel,
                ':no_entry_sign: {}: Please specify an integer next time.'.format(message.author.name)
                )
            cont = False
    else:
        r = 0

    try:
        with open('configs/quotes.json') as z:
            quotes = json.load(z)
    except FileNotFoundError:
        await client.send_message(message.channel, 'I do not have any quotes to remove.')
        cont = False

    if cont:
        if message.author.id == quotes[r - 1][1] or message.author.id == base.config['owner_id']:
            quotes.pop(r - 1)
            with open('configs/quotes.json', 'w') as z:
                json.dump(quotes, z, indent=4)

            if r == 0:
                r = len(quotes)+1

            await client.send_message(
                message.channel,
                ':heavy_check_mark: {}: Quote #{} has been removed.'.format(
                    message.author.name,
                    r
                )
            )
        else:
            await client.send_message(
                message.channel,
                ':no_entry_sign: You did not create that quote.'
                )
delquote.server = 'Quotes'

@base.cacofunc
async def parsequote(message, client):
    '''
    **{0}parsequote**
    This command is under renovations.
    *Example: `{0}parsequote`*
    '''
    await client.send_messag(message.channel, ':no_entry_sign: This command is under renovations.')
parsequote.server = 'Quotes'

# Logging

def date_format(timestamp):
    '''Format a timestamp as Month DD, YYYY'''
    months = [
        'MISSINGMO', # :^)
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]
    return '{} {}, {}'.format(
        months[timestamp.month],
        timestamp.day,
        timestamp.year
        )

@base.cacofunc
async def log(message, client):
    '''
    **{0}log** [*req*]
    Sends the last 20 messages in a channel to you in a direct message in a nice, copy-pastable format. You can specify [*req*] to get a specific number of messages. (This is subject to limitations emposed by the API and the bot maintainer's preference.)
    *Example: `{0}log 25`*
    '''

    # Check to see how many messages we should grab.
    params = message.content.split()
    if len(params) > 1:
        req = int(params[1])
    else:
        req = 20

    #Do not continue if requests is over the limit.
    if req > base.config['log_request_limit']:
        await client.send_message(
            message.channel,
            '{}: That\'s way too many messages to send, as decreed by my creator. Acceptable amounts end at {}.'.format(
                message.author,
                base.config['log_request_limit']
                )
            )
        return

    if req < 1:
        await client.send_message(message.channel, '{}: Very clever, smart ass. Type a whole number next time.'.format(message.author.mention))
        return

    requests = int(req) + 1 #Because logs_from will get the last message (which will be ".logs x"), we anticipate that here.

    #Yes you're reading that right. We get an iterator, convert it to a list, reverse it, and then convert THAT to a list so we can len() it.
    #This is because len() doesn't work on iterators, and logs_from returns messages starting from the newest one.

    #Thanks to async for we have to do this manually
    msg_iter = []
    async for x in client.logs_from(message.channel, requests):
        msg_iter.append(x)

    messages = list(reversed(msg_iter))

    # This string will hold the log we are going to send in each message, and will be blanked after each message.
    msgToSend = ''
    # This string will hold the message we are adding to msgToSend, and will be used to test if the length of msgToSend will be >2000 characters if we add it.
    msgToAdd = ''

    # send each message back with proper timestamp and username trailing
    for iteration, x in enumerate(messages):
        # Create long timestamp from first message.
        if iteration == 0:
            msgToSend = date_format(x.timestamp) + '\n'

        if iteration != len(messages) - 1: # ensure the ".log" message doesn't send

            # Timestamps don't have a trailing 0 on time objects, so this will give one to the minute time object.
            minute = '00'
            if len(str(x.timestamp.minute)) != 2:
                minute = '0' + str(x.timestamp.minute)
            else:
                minute = str(x.timestamp.minute)

            # Send attachments
            if x.attachments:
                msgToAdd += '{}:{} - {}:\n'.format(
                    x.timestamp.hour,
                    minute,
                    x.author.name,
                    )

                if x.content:
                    msgToAdd += message.content

                for ach in x.attachments:
                    msgToAdd += '\n{}'.format(ach['url'])

            # Send message
            else:
                msgToAdd = '{}:{} - {}: {}\n'.format(
                    x.timestamp.hour,
                    minute,
                    x.author.name,
                    x.content.replace('*', r'\*').replace('_', r'\_').replace('~', r'\~').replace('`', r'\`')
                    )

            if len(msgToSend + msgToAdd) < 2000:
                msgToSend += msgToAdd
            else:
                await client.send_message(message.author, msgToSend)
                msgToSend = msgToAdd
                await asyncio.sleep(5)

            if iteration == len(messages) - 2:
                await client.send_message(message.author, msgToSend)

@base.cacofunc
async def logquote(message, client):
    '''
    **{0}logquote** [*num*] [*slice*]
    Takes the last *num* quotes, and then adds them to the Quotes list, after OKaying it with you. If *slice* is provided, the quote will take the last *num* messages up to the last *slice* messages. For example, `{0}logquote 4 2` would quote the 4th to last, 3rd to last, and 2nd to last messages.
    *Example: `{0}logquote 10 6`*
    '''
    r = None
    s = None

    if len(message.content.split()) > 1:
        try:
            r = int(message.content.split()[1])
            if len(message.content.split()) > 2: # slice
                try:
                    s = int(message.content.split()[2])
                except ValueError:
                    await client.send_message(
                        message.channel,
                        '{}: Please provide an integer to slice.'.format(
                            message.author.name
                        )
                    )
                    return
            else:
                s = 1
        except ValueError:
            await client.send_message(message.channel, 'Please provide an integer to log.')
            return
    else:
        await client.send_message(message.channel, 'Please provide a numeric index or slice.')
        return


    msg_iter = []
    async for x in client.logs_from(message.channel, r + 1):
        msg_iter.append(x)
    messages = list(reversed(list(msg_iter)))

    msgToAdd = ''

    for iteration, x in enumerate(messages):
        if iteration == 0:
            msgToAdd = date_format(x.timestamp) + '\n'

        if iteration < len(messages) - s:

            minute = '00'
            if len(str(x.timestamp.minute)) != 2:
                minute = '0' + str(x.timestamp.minute)
            else:
                minute = str(x.timestamp.minute)

            # log attachments
            if x.attachments:
                msgToAdd += '{}:{} - {}:\n'.format(
                    x.timestamp.hour,
                    minute,
                    x.author.name,
                    )

                if x.content:
                    msgToAdd += message.content

                for ach in x.attachments:
                    msgToAdd += '\n{}'.format(ach['url'])

            # log message
            else:
                msgToAdd += '{}:{} - {}: {}\n'.format(
                    x.timestamp.hour,
                    minute,
                    x.author.name,
                    x.content
                    )


    #replace mentions
    while mention_syntax.search(msgToAdd):
        member = discord.utils.get(
            message.server.members,
            id=mention_syntax.search(msgToAdd).group(2)
            )

        if member:
            msgToAdd = msgToAdd.replace(
                mention_syntax.search(msgToAdd).group(1),
                '@' + member.name)
        else:
            msgToAdd = msgToAdd.replace(
                mention_syntax.search(msgToAdd).group(1),
                '@invalid_user'
            )

    cmd = msgToAdd.replace('@everyone', '@\u2020everyone').replace('@here', '@\u2020here')

    if not msgToAdd:
        await client.send_message(message.channel, ':no_entry_sign: I ended up logging nothing, so I added nothing to my quotes.')
        return

    if len(msgToAdd) >= 1897:
        await client.send_message(message.channel, ':no_entry_sign: There is too much text for me to log here.')
        return

    await client.send_message(message.channel, 'Confirm my selection in DMs, please.')
    await client.send_message(message.author, 'I have logged the following message:\n{}\nIf this looks correct to you, please respond "Yes". If not, respond "No."'.format(msgToAdd))

    loop = True
    while loop:
        msg = await client.wait_for_message(author=message.author, check=lambda msg: msg.channel.is_private)
        if msg.content.lower() == 'no':
            await client.send_message(message.author, 'I have discarded that quote. My apologies.')
            return
        elif msg.content.lower() != 'yes':
            await client.send_message(message.author, 'Please respond either "Yes" or "No"')
        else:
            loop = False

            # open quotes file. Make file if it doesn't exist
            quotes = []
            try:
                with open('configs/quotes.json') as z:
                    quotes = json.load(z)
            except FileNotFoundError:
                with open('configs/quotes.json', 'w') as z:
                    z.write('[]')

            quotes.append([msgToAdd, message.author.id])

            # Save file.
            with open('configs/quotes.json', 'w') as z:
                json.dump(quotes, z, indent=4)

            await client.send_message(
                message.author,
                '{}: :heavy_check_mark: Successfully added that to my quote database as quote number {}.'.format(
                    message.author,
                    len(quotes)
                    )
                )

            await client.send_message(
                message.channel,
                '{}: :heavy_check_mark: Successfully added that to my quote database as quote number {}.'.format(
                    message.author,
                    len(quotes)
                    )
                )
logquote.server = 'Quotes'

@base.cacofunc
async def memo(message, client):
    '''
    **{0}memo** [ all | mentions | none ]
    Manages your inclusion into the memoing system.
    `all` will DM you both mentions, and everyone mentions.
    `mentions` will only DM you if someone mentions you specifically.
    `none` removes you from the memoing system.
    If you are on the memoing system and you are mentioned in a channel that this bot is in, and you are not online, this bot will DM you where the mention was recieved (server and channel) plus the last 5 messages in that channel for context.
    *Example: `{0}memo add`*
    '''

    try:
        cmd = message.content.split()[1]

        # Load memo list. This is created automatically when a mention is
        # in a message.
        with open('configs/memos.json') as z:
            memos = json.load(z)

        if cmd == 'all':
            if not [x for x in memos if message.author.id == x[0]]:
                memos.append([message.author.id, 'all'])
                await client.send_message(
                    message.author,
                    ':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when you are, or everyone is, mentioned.'
                    )
            elif [x for x in memos if message.author.id == x[0] and x[1] != 'all']:
                memos.remove([x for x in memos if message.author.id == x[0] and x[1] != 'all'][0])
                memos.append([message.author.id, 'all'])
                await client.send_message(
                    message.author,
                    ':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when you are, or everyone is, mentioned.'
                    )
            else:
                await client.send_message(
                    message.author,
                    ':no_entry_sign: You are already on the memo list.'
                    )

        elif cmd == 'mentions':
            if not [x for x in memos if message.author.id == x[0]]:
                memos.append([message.author.id, 'mentions'])
                await client.send_message(
                    message.author,
                    ':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when you are mentioned.'
                    )
            elif [x for x in memos if message.author.id == x[0] and x[1] != 'mentions']:
                memos.remove([x for x in memos if message.author.id == x[0] and x[1] != 'mentions'][0])
                memos.append([message.author.id, 'mentions'])
                await client.send_message(
                    message.author,
                    ':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when specifically you are mentioned.'
                    )
            else:
                await client.send_message(
                    message.author,
                    ':no_entry_sign: You are already on the memo list.'
                    )

        elif cmd == 'remove':
            if [x for x in memos if message.author.id == x[0]]:
                memos.remove([x for x in memos if message.author.id == x[0]][0])
                await client.send_message(
                    message.author,
                    ':no_bell: You have been removed from the memo list.'
                    )
            else:
                await client.send_message(
                    message.author,
                    ':no_entry_sign: You are not on the memo list.'
                    )
        else:
            raise IndexError('User did not specify a valid command.') # Boy howdy am I lazy.

        # Save memo list.
        with open('configs/memos.json', 'w') as z:
            json.dump(memos, z, indent=4)

    except IndexError:
        await client.send_message(message.channel, ':no_entry_sign: You must specify wether I should memo you **all** or **mentions**, or if I should **remove** you from the memo list.')

@base.postcommand
async def sendmemo(message, client):
    if message.mentions: # False if no mentions
        # Load memo list
        memos = {}
        try:
            with open('configs/memos.json') as z:
                memos = json.load(z)
        except FileNotFoundError:
            with open('configs/memos.json', 'w') as z:
                json.dump(memos, z, indent=4)

        msgme = []

        for mention in message.mentions:
            # The async branch turned status into an enum. It's nice.
            # If the mentioned user is not online, signed up for memos, and is able to see the channel:
            if mention.id in [x[0] for x in memos] and mention.status != discord.Status.online and message.channel.permissions_for(mention).read_messages:
                # Store user for later messaging.
                msgme.append(mention)

        # await is weird: You can only call it in specific
        # places. Here we reverse a log of the last 5 messages.
        if msgme:
            msg_iter = []
            async for x in client.logs_from(message.channel, 5):
                msg_iter.append(x)
            thislog = reversed(list(msg_iter))
            # If your net/computer is slow enough, sometimes you'll
            # get a few messages after the mention. Deal with it.
            msgToSend = '**You were mentioned in {}\'s #{} channel.** Here is the context:\n'.format(message.server.name, message.channel.name)

            # refer to log.py for info on how this works:
            for x in thislog:
                minute = '00'
                if len(str(x.timestamp.minute)) != 2:
                    minute = '0' + str(x.timestamp.minute)
                else:
                    minute = str(x.timestamp.minute)
                msgToSend += '{}:{} - {}: {}\n'.format(
                    x.timestamp.hour,
                    minute,
                    x.author.name,
                    x.content
                    )

            for mention in msgme:
                await client.send_message(mention, msgToSend[:1980]) # Really shitty way of making sure it's beneath 2k characters but IT WORKS, SO CAN IT
                asyncio.sleep(5)

    if '@everyone' in message.content and message.channel.permissions_for(message.author).mention_everyone:

        # Load memo list
        memos = {}
        try:
            with open('configs/memos.json') as z:
                memos = json.load(z)
        except FileNotFoundError:
            with open('configs/memos.json', 'w') as z:
                json.dump(memos, z, indent=4)

        msgme = []
        for mem in [x[0] for x in memos if x[1] == 'all']:
            # Find member object based on id
            usr = discord.utils.find(lambda x: x.id == mem, message.server.members)
            # Prevent mentions in cannels people can't read from being sent
            if usr != None and message.channel.permissions_for(usr).read_messages and usr.status != discord.Status.online:
                msgme.append(usr)

        if msgme:
            msg_iter = []
            async for x in client.logs_from(message.channel, 5):
                msg_iter.append(x)
            thislog = reversed(list(msg_iter))

            msgToSend = '**Someone used @everyone in {}\'s #{} channel.** Here is the context:\n'.format(message.server.name, message.channel.name)

            # refer to log.py for info on how this works:
            for x in thislog:
                minute = '00'
                if len(str(x.timestamp.minute)) != 2:
                    minute = '0' + str(x.timestamp.minute)
                else:
                    minute = str(x.timestamp.minute)
                msgToSend += '{}:{} - {}: {}\n'.format(
                    x.timestamp.hour,
                    minute,
                    x.author.name,
                    x.content
                    )

            for mention in msgme:
                await client.send_message(mention, msgToSend[:1980])
                asyncio.sleep(5)
