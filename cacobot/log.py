import cacobot.base as base
import json, asyncio

# Open the config to get log request limit.
with open('configs/config.json') as data:
    config = json.load(data)

def date_format(timestamp):
    """Format a timestamp as Month DD, YYYY"""
    months = [
      'ERRMONTH',
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
    """
    **.log** [*req*]
    Sends the last 20 messages in a channel to you in a direct message in a nice, copy-pastable format. You can specify [*req*] to get a specific number of messages. (This is subject to limitations emposed by the API and the bot maintainer's preference.)
    *Example: .log 25*
    """

    # Check to see how many messages we should grab.
    params = message.content.split(" ")
    if len(params) > 1:
        req = int(params[1])
    else:
        req = 20

    #Do not continue if requests is over the limit.
    if req > config['log_request_limit']:
        yield from client.send_message(
          message.channel,
          "{}: That's way too many messages to send, as decreed by my creator. Acceptable amounts end at {}.".format(
             message.author.mention(),
             str(config['log_request_limit'])
          )
        )
    elif req < 1:
        yield from client.send_message(message.channel, "{}: Very clever, smart ass. Type a whole number next time.".format(message.author.mention()))
    else:
        requests = int(req) + 1 #Because logs_from will get the last message (which will, invariably, be ".logs x"), we anticipate that here.

        #Yes you're reading that right. We get an iterator, convert it to a list, reverse it, and then convert THAT to a list so we can len() it.
        #This is because len() doesn't work on iterators, and logs_from returns messages starting from the newest one.
        msg_iter = yield from client.logs_from(message.channel, requests)
        messages = list(reversed(list(msg_iter)))

        #send each message back with proper timestamp and username trailing
        for iteration, x in enumerate(messages):
            #Create long timestamp from first message.
            if iteration == 0:
                yield from client.send_message(message.author, date_format(x.timestamp))

            if iteration != len(messages) - 1: # ensure the ".log" message doesn't send

                #Timestamps don't have a trailing 0 on time objects, so this will give one to the minute time object.
                minute = '00'
                if len(str(x.timestamp.minute)) != 2:
                    minute = '0' + str(x.timestamp.minute)
                else:
                    minute = str(x.timestamp.minute)

                # Send attachments
                if x.attachments:
                    for ach in x.attachments:
                        yield from client.send_message(message.author, '{}:{} - {}: {}\n'.format(
                          str(x.timestamp.hour),
                          minute,
                          x.author.name,
                          ach['url']))

                # Send message
                else:
                    yield from client.send_message(message.author, '{}:{} - {}: {}\n'.format(
                      str(x.timestamp.hour),
                      minute,
                      x.author.name,
                      x.content))

                yield from asyncio.sleep(3000)
