import cacobot.base as base
import json, random

@base.cacofunc
def quote(message, client, *args, **kwargs):
    '''
    **.quote** [*id*]
    Spews a random quote from my database. If *id* is provided, spews the quote with that id.
    *Example: `.quote 1`*
    '''
    cont = True

    if len(message.content.split(' ')) != 1:
        r = int(message.content.split(' ')[1])
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
            yield from client.send_message(message.channel, '*This is quote {} {}:*\n{}'.format(random.choice(['number', 'nombre', 'numero']), qindex, quotes[qindex-1]))
        elif r < 1:
            yield from client.send_message(message.channel, 'You probably think you\'re really clever. Specify a *positive* quote index next time. Better yet: specify none at all for a random quote.')
        elif r > len(quotes):
            yield from client.send_message(message.channel, ':no_entry_sign: You have specified a quote index that is too high. I only have {} quotes to puke.'.format(len(quotes)))
        else:
            yield from client.send_message(message.channel, quotes[r-1])

@base.cacofunc
def addquote(message, client, *args, **kwargs):
    '''
    **addquote** <*content*>
    Add a quote to my quote database.
    *Example: `.addquote <TerminusEst13> .idgames good map
    <idgamesbot> Nothing found.
    <TerminusEst13> Well there you have it, folks.`*
    '''
    cmd = message.content.split(' ', 1)[1]

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
                json.dump(quotes, data, indent=4)

        if cmd not in quotes:
        # Add quote to list
            quotes.append(cmd)

            # Save file.
            with open('configs/quotes.json', 'w') as data:
                json.dump(quotes, data, indent=4)

            yield from client.send_message(message.channel, '{}: Successfully added that to my quote database as quote number {}.'.format(message.author.mention, str(len(quotes))))
        else:
            yield from client.send_message(message.channel, '{}: I already have that exact quote in my database.'.format(message.author.mention))
