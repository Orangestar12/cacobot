import random
import cacobot.base as base

@base.postcommand
async def woah(message, client):
    c = message.content.lower()
    send = None
    if message.author.id != client.user.id:
        if c == 'woah' or\
                c == 'woah.' or\
                c == 'whoa' or\
                 c == 'whoa.':
            send = 'Hey guys.'
        elif c == 'hey guys' or c == 'hey guys':
            send = 'Welcome to EB Games.'
        elif 'call of duty' in c or\
                'advanced warfare' in c or\
                'xbox one' in c:
            send = 'Copy that.'

    if send:
        if random.randint(1, 20) == 1:
            await client.send_message(message.channel, send)

@base.postcommand
async def wow(message, client):
    c = message.content.lower()
    if message.author.id != client.user.id:
        if c == 'wow' or c == 'wow.':
            if random.randint(1, 20) == 1:
                await client.send_message(
                    message.channel,
                    'Ethan, great moves. Keep it up. I\'m proud of you.'
                    )
