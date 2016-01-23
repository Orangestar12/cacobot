import cacobot.base as base
import json, random, re, discord

with open('configs/config.json') as data:
    config = json.load(data)

mention_syntax = re.compile('(<@([0-9]*?)>)')

@base.cacofunc
def quote(message, client, *args, **kwargs):
    '''
    **.quote** [*id*]
    Spews a random quote from my database. If *id* is provided, spews the quote with that id.
    *Example: `.quote 1`*
    '''
    cont = True

    if '.' in message.content[1:]:
        yield from client.send_message(message.channel, '2:23 AM - 🎮 Mr McPowned: @KeksGiven to be fair, he can\'t store floats\n2:23 AM - 🎮 Mr McPowned: And if he did, I\'d call him retarded')
        cont = False

    if len(message.content.split(' ')) != 1:
        try:
            r = int(message.content.split(' ')[1])
        except ValueError:
            yield from client.send_message(message.channel, ':no_entry_sign: Please specify an integer next time.')
            cont = False
    else:
        r = 0

    try:
        with open('configs/quotes.json') as data:
            quotes = json.load(data)
    except FileNotFoundError:
        yield from client.send_message(message.channel, 'I do not have any quotes to puke.')
        cont = False

    if cont:
        if r == 0:
            qindex = random.randint(0, len(quotes))
            yield from client.send_message(message.channel, '*This is quote {}{}:*\n{}'.format(random.choice(['number ', 'numero ', 'numbuh ', '#', 'integer ', '№ ']), qindex, quotes[qindex-1][0]))
        elif r < 1:
            yield from client.send_message(message.channel, 'You probably think you\'re really clever. Specify a *positive* quote index next time. Better yet: specify none at all for a random quote.')
        elif r > len(quotes):
            yield from client.send_message(message.channel, ':no_entry_sign: You have specified a quote index that is too high. I only have {} quotes to puke.'.format(len(quotes)))
        else:
            yield from client.send_message(message.channel, quotes[r-1][0])
quote.server = 'Quotes'

@base.cacofunc
def addquote(message, client, *args, **kwargs):
    '''
    **addquote** <*content*>
    Add a quote to my quote database.
    *Example: `.addquote <TerminusEst13> .idgames good map
    <idgamesbot> Nothing found.
    <TerminusEst13> Well there you have it, folks.`*
    '''
    cmd = message.content.split(' ', 1)[1].strip()

    # Complain about cheeky asses.

    if cmd.startswith('.addquote'):
        yield from client.send_message(message.channel, '{}: Hah hah, very funny, but that wouldn\'t work anyway.'.format(message.author.mention))

    elif cmd.startswith('.quote'):
        yield from client.send_message(message.channel, '{}: Not only would that not work, but that\'s really annoying. Stop that shit.'.format(message.author.mention))

    else: # Actually add a quote

        # open quotes file. Make file if it doesn't exist
        quotes = []
        try:
            with open('configs/quotes.json') as data:
                quotes = json.load(data)
        except FileNotFoundError:
            with open('configs/quotes.json', 'w') as data:
                data.write('[]')

        if not [x[0] for x in quotes if x[0] == cmd]:
            # Add quote to list
            #replace mentions
            if mention_syntax.search(cmd):
                cmd = cmd.replace(mention_syntax.search(cmd).group(1), '@' + discord.utils.get(message.server.members, id=mention_syntax.search(cmd).group(2)).name)

            quotes.append([cmd, message.author.id])

            # Save file.
            with open('configs/quotes.json', 'w') as data:
                json.dump(quotes, data, indent=4)

            if cmd.startswith('http://') or cmd.startswith('https://'):
                yield from client.send_message(message.channel, '{}: :warning: I have added that quote successfully as number {}, but couldn\'t help noticing it starts with a link. If this is an image of a Discord chat log, consider providing your quotes as text next time, or using my `.log` function.'.format(message.author.mention, str(len(quotes))))
            else:
                yield from client.send_message(message.channel, '{}: :heavy_check_mark: Successfully added that to my quote database as quote number {}.'.format(message.author.mention, str(len(quotes))))
        else:
            yield from client.send_message(message.channel, '{}: :no_entry_sign: I already have that exact quote in my database.'.format(message.author.mention))
addquote.server = 'Quotes'

@base.cacofunc
def delquote(message, client, *args, **kwargs):
    '''
    **.delquote** [*index*]
    Removes a quote from the database. You can only remove quotes you have created. Specify no index to try to remove the last quote.
    *Example: `.delquote 13`*
    '''

    cont = True

    if len(message.content.split(' ')) != 1:
        try:
            r = int(message.content.split(' ')[1])
        except ValueError:
            yield from client.send_message(message.channel, ':no_entry_sign: Please specify an integer next time.')
            cont = False
    else:
        r = 0

    try:
        with open('configs/quotes.json') as data:
            quotes = json.load(data)
    except FileNotFoundError:
        yield from client.send_message(message.channel, 'I do not have any quotes to remove.')
        cont = False

    if cont:
        if message.author.id == quotes[r - 1][1] or message.author.id == config['owner_id']:
            quotes.pop(r - 1)
            with open('configs/quotes.json', 'w') as data:
                json.dump(quotes, data, indent=4)

            if r == 0:
                r = len(quotes)+1

            yield from client.send_message(message.channel, ':heavy_check_mark: {}: Quote #{} has been removed.'.format(message.author.mention, r))
        else:
            yield from client.send_message(message.channel, ':no_entry_sign: You did not create that quote.')
delquote.server = 'Quotes'

@base.cacofunc
def parsequote(message, client, *args, **kwargs):
    '''
    **.parsequote** [*index*]
    Takes a log selected wholesale from a Discord window, and adds it to the quote database neatly formatted. This will only work with quotes that have a timestamp labeled "Today"
    *Example: `.parsequote December 27, 2015
    xgmToday at 5:29 PM
    HI EVERYONE I ROLEPLAY AS AN ALARM CLOCK
    **AAAAAHHHHHHHHH**`*
    '''
    cont = True

    try:
        cmd = message.content.strip().split(' ', 1)[1].split('\n')
    except IndexError:
        yield from client.send_message(message.channel, ':no_entry_sign: You did not provide a quote to parse.')
        cont = False

    if cont:
        # This array holds each line of the quote we will add. It will be joined with \n.
        qToAdd = []

        # This holds the name of the person saying the quote, which we derive from headers.
        name = ''

        for x in cmd:
            if x != '' and x != 'NEW MESSAGES': #Strip "New Messages" thing and any empty lines. Pray to god nobody ever types "NEW MESSAGES".
                try:
                    # Detect Timestamp
                    # Is this three parts? (Month XX, YYYY)
                    if len(x.split(' ')) == 3:
                        # Is the first part a month?
                        if x.split(' ')[0] in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
                            # Is the second part a number followed by a comma?
                            int(x.split(' ')[1][:-1]) #If the second part is not a number, a ValueError will be raised.
                            if x.split(' ')[1][-1] == ',':
                                # Is the third part a 4-digit number?
                                int(x.split(' ')[2])
                                if len(x.split(' ')[2]) == 4:
                                    qToAdd.append(x)
                                else:
                                    raise ValueError
                            else:
                                raise ValueError
                        else:
                            raise ValueError
                    else:
                        raise ValueError
                    # Yes, I'm glad you recognized that was the worst way to handle it.
                except ValueError:
                    # Not a timestamp: See if this is a message header.

                    cont = True
                    # This looks for "Today at XX:XX AM/PM" without regex.
                    # I wouldn't doubt the re module could do it better but re is so unweildy
                    if 'Today at ' in x and (x.endswith(' AM') or x.endswith(' PM')):
                        try:
                            # check for valid integer before and after timestamp
                            int(x.split(' ')[-2].split(':')[0])
                            int(x.split(' ')[-2].split(':')[1])

                            # We still here? Ding ding ding, we have a header!
                            tI = x.rfind("Today")
                            usrnm = x[:tI]
                            name = '{} - {}'.format(x.split(' ')[-2] + x.split(' ')[-1], usrnm)

                            cont = False

                        except (ValueError, IndexError):
                            pass

                    if cont:
                        qToAdd.append('{}: {}'.format(name, x))

        if qToAdd:
            # open quotes file. Make file if it doesn't exist
            quotes = []
            try:
                with open('configs/quotes.json') as data:
                    quotes = json.load(data)
            except FileNotFoundError:
                with open('configs/quotes.json', 'w') as data:
                    data.write('[]')

            cmd = '\n'.join(qToAdd)

            if mention_syntax.search(cmd):
                cmd = cmd.replace(mention_syntax.search(cmd).group(1), '@' + discord.utils.get(message.server.members, id=mention_syntax.search(cmd).group(2)).name)

            quotes.append([cmd, message.author.id])

            with open('configs/quotes.json', 'w') as data:
                json.dump(quotes, data, indent=4)
            yield from client.send_message(message.channel, ':heavy_check_mark: {}: Successfully parsed and added that as quote number {}.'.format(message.author.mention, len(quotes)))

        else:
            yield from client.send_message(message.channel, ':no_entry_sign: Something weird happened when I parsed that quote: Everything you sent me was stripped out. (This could happen if the message was just "NEW MESSAGES" or something equally stupid you did to test me.)\nThe quote has not been added.')
parsequote.server = 'Quotes'
