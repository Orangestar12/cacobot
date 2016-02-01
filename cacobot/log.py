import cacobot.base as base
import json, asyncio, discord

# Open the config to get log request limit.
with open('configs/config.json') as data:
    config = json.load(data)

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
      str(months[timestamp.month]),
      str(timestamp.day),
      str(timestamp.year)
    )

@base.cacofunc
def log(message, client, *args, **kwargs):
    '''
    **.log** [*req*]
    Sends the last 20 messages in a channel to you in a direct message in a nice, copy-pastable format. You can specify [*req*] to get a specific number of messages. (This is subject to limitations emposed by the API and the bot maintainer's preference.)
    *Example: `.log 25`*
    '''

    # Check to see how many messages we should grab.
    params = message.content.split(' ')
    if len(params) > 1:
        req = int(params[1])
    else:
        req = 20

    #Do not continue if requests is over the limit.
    if req > config['log_request_limit']:
        yield from client.send_message(
          message.channel,
          '{}: That\'s way too many messages to send, as decreed by my creator. Acceptable amounts end at {}.'.format(
             message.author.mention,
             str(config['log_request_limit'])
          )
        )
    elif req < 1:
        yield from client.send_message(message.channel, '{}: Very clever, smart ass. Type a whole number next time.'.format(message.author.mention))
    else:
        requests = int(req) + 1 #Because logs_from will get the last message (which will be ".logs x"), we anticipate that here.

        #Yes you're reading that right. We get an iterator, convert it to a list, reverse it, and then convert THAT to a list so we can len() it.
        #This is because len() doesn't work on iterators, and logs_from returns messages starting from the newest one.
        msg_iter = yield from client.logs_from(message.channel, requests)
        messages = list(reversed(list(msg_iter)))

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
                    for ach in x.attachments:
                        msgToAdd = '{}:{} - {}: {}\n'.format(
                          x.timestamp.hour,
                          minute,
                          x.author.name,
                          ach['url'])

                # Send message
                else:
                    msgToAdd = '{}:{} - {}: {}\n'.format(
                      str(x.timestamp.hour),
                      minute,
                      x.author.name,
                      x.content.replace('*', '\*').replace('_', '\_').replace('~', '\~').replace('`', '\`')
                  )

                if len(msgToSend + msgToAdd) < 2000:
                    msgToSend += msgToAdd
                else:
                    yield from client.send_message(message.author, msgToSend)
                    msgToSend = msgToAdd
                    yield from asyncio.sleep(5)

                if iteration == len(messages) - 2:
                    yield from client.send_message(message.author, msgToSend)



@base.cacofunc
def memo(message, client, *args, **kwargs):
    '''
    **.memo** [ all | mentions | none ]
    Manages your inclusion into the memoing system.
    `all` will DM you both mentions, and everyone mentions.
    `mentions` will only DM you if someone mentions you specifically.
    `none` removes you from the memoing system.
    If you are on the memoing system and you are mentioned in a channel that this bot is in, and you are not online, this bot will DM you where the mention was recieved (server and channel) plus the last 5 messages in that channel for context.
    *Example: `.memo add`*
    '''

    try:
        cmd = message.content.split(' ')[1]

        # Load memo list. This is created automatically when a mention is
        # in a message.
        with open('configs/memos.json') as data:
            memos = json.load(data)

        if cmd == 'all':
            if not [x for x in memos if message.author.id == x[0]]:
                memos.append([message.author.id, 'all'])
                yield from client.send_message(message.author,':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when you are, or everyone is, mentioned.')
            elif [x for x in memos if message.author.id == x[0] and 'all' != x[1]]:
                memos.remove([x for x in memos if message.author.id == x[0] and 'all' != x[1]][0])
                memos.append([message.author.id, 'all'])
                yield from client.send_message(message.author,':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when you are, or everyone is, mentioned.')
            else:
                yield from client.send_message(message.author,':no_entry_sign: You are already on the memo list.')
        elif cmd == 'mentions':
            if not [x for x in memos if message.author.id == x[0]]:
                memos.append([message.author.id, 'mentions'])
                yield from client.send_message(message.author,':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when you are mentioned.')
            elif [x for x in memos if message.author.id == x[0] and 'mentions' != x[1]]:
                memos.remove([x for x in memos if message.author.id == x[0] and 'mentions' != x[1]][0])
                memos.append([message.author.id, 'mentions'])
                yield from client.send_message(message.author,':notebook_with_decorative_cover: You are now on the memo list and will recieve direct messages with context when specifically you are mentioned.')
            else:
                yield from client.send_message(message.author,':no_entry_sign: You are already on the memo list.')
        elif cmd == 'remove':
            if [x for x in memos if message.author.id == x[0]]:
                memos.remove([x for x in memos if message.author.id == x[0]][0])
                yield from client.send_message(message.author,':no_bell: You have been removed from the memo list.')
            else:
                yield from client.send_message(message.author,':no_entry_sign: You are not on the memo list.')
        else:
            raise IndexError('User did not specify a valid command.') # Boy howdy am I lazy.

        # Save memo list.
        with open('configs/memos.json', 'w') as data:
            json.dump(memos, data, indent=4)

    except IndexError:
        yield from client.send_message(message.channel, ':no_entry_sign: You must specify wether I should **add** or **remove** you from the memo list.')

@base.postcommand
def sendmemo(message, client, *args, **kwargs):
    if message.mentions: # False if no mentions
        # Load memo list
        memos = {}
        try:
            with open('configs/memos.json') as data:
                memos = json.load(data)
        except FileNotFoundError:
            with open('configs/memos.json', 'w') as data:
                json.dump(memos, data, indent=4)

        msgme = []

        for mention in message.mentions:
            # The async branch turned status into an enum. It's nice.
            # If the mentioned user is not online, signed up for memos, and is able to see the channel:
            if mention.id in [x[0] for x in memos] and mention.status != discord.Status.online and message.channel.permissions_for(mention).read_messages:
                # Store user for later messaging.
                msgme.append(mention)

        # yield from is weird: You can only call it in specific
        # places. Here we reverse a log of the last 5 messages.
        if msgme:
            log = yield from client.logs_from(message.channel, 5)
            log = reversed(list(log))
            # If your net/computer is slow enough, sometimes you'll
            # get a few messages after the mention. Deal with it.
            msgToSend = '**You were mentioned in {}\'s #{} channel.** Here is the context:\n'.format(message.server.name, message.channel.name)

            # refer to log.py for info on how this works:
            for x in log:
                minute = '00'
                if len(str(x.timestamp.minute)) != 2:
                    minute = '0' + str(x.timestamp.minute)
                else:
                    minute = str(x.timestamp.minute)
                msgToSend += '{}:{} - {}: {}\n'.format(
                  str(x.timestamp.hour),
                  minute,
                  x.author.name,
                  x.content
                )

            for mention in msgme:
                yield from client.send_message(mention, msgToSend[:1980]) # Really shitty way of making sure it's beneath 2k characters but IT WORKS, SO CAN IT
                asyncio.sleep(5)

    if message.mention_everyone: # @everyone

        # Load memo list
        memos = {}
        try:
            with open('configs/memos.json') as data:
                memos = json.load(data)
        except FileNotFoundError:
            with open('configs/memos.json', 'w') as data:
                json.dump(memos, data, indent=4)

        msgme = []
        for mem in [x[0] for x in memos if x[1] == 'all']:
            # Find member object based on id
            usr = discord.utils.find(lambda x: x.id == mem, message.server.members)
            # Prevent mentions in cannels people can't read from being sent
            if usr != None and message.channel.permissions_for(usr).read_messages and usr.status != discord.Status.online:
                msgme.append(usr)

        if msgme:
            log = yield from client.logs_from(message.channel, 5)
            log = reversed(list(log))

            msgToSend = '**Someone used \@everyone in {}\'s #{} channel.** Here is the context:\n'.format(message.server.name, message.channel.name)

            # refer to log.py for info on how this works:
            for x in log:
                minute = '00'
                if len(str(x.timestamp.minute)) != 2:
                    minute = '0' + str(x.timestamp.minute)
                else:
                    minute = str(x.timestamp.minute)
                msgToSend += '{}:{} - {}: {}\n'.format(
                  str(x.timestamp.hour),
                  minute,
                  x.author.name,
                  x.content)

            for mention in msgme:
                yield from client.send_message(mention, msgToSend[:1980])
                asyncio.sleep(5)
