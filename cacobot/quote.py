import cacobot.base as base
import json, random

@base.cacofunc
def quote(message, client, *args, **kwargs):
    """
    **.quote** [*id*]
    Spews a random quote from my database. If *id* is provided, spews the quote with that id.
    *Example: .quote 1*
    """
    if len(message.content.split(' ')) != 1:
        r = int(message.content.split(' ')[1])
    else:
        r = 0

    with open('configs/quotes.json') as data:
        quotes = json.load(data)

    if r == 0:
        yield from client.send_message(message.channel, quotes[random.randint(0, len(quotes)-1)])
    else:
        yield from client.send_message(message.channel, quotes[r-1])

@base.cacofunc
def addquote(message, client, *args, **kwargs):
    """
    **addquote** <*content*>
    Add a quote to my quote database.
    *Example: .addquote <TerminusEst13> .idgames good map
    <idgamesbot> Nothing found.
    <TerminusEst13> Well there you have it, folks.*
    """
    cmd = message.content.split(' ', 1)[1]

    # Complain about cheeky asses.

    if cmd.startswith(".addquote"):
        yield from client.send_message(message.channel, "{}: Hah hah, very funny, but that wouldn't work anyway.".format(message.author.mention))

    elif cmd.startswith(".quote"):
        yield from client.send_message(message.channel, "{}: Not only would that not work, but that's really annoying. Stop that shit.".format(message.author.mention))

    else: # Actually add a quote

        # open quotes file. Make file if it doesn't exist
        quotes = {}
        try:
            with open('configs/quotes.json') as data:
                quotes = json.load(data)
        except FileNotFoundError:
            with open('configs/quotes.json', 'w') as data:
                json.dump(quotes, data, indent=4)

        # Add quote to dictionary
        quotes.append(cmd)

        # Save file.
        with open('configs/quotes.json', 'w') as data:
            json.dump(quotes, data, indent=4)

        yield from client.send_message(message.channel, "{}: Successfully added that to my quote database as quote number {}.".format(message.author.mention, str(len(quotes))))
