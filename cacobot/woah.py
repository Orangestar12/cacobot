import cacobot.base as base
import asyncio, random

@base.postcommand
def woah(message, client, *args, **kwargs):
    if random.randint(0, 9000) == 1366:
        if message.author.id != client.user.id:
            if message.content.lower() == 'woah' or message.content.lower() == 'woah.' or message.content.lower() == 'whoa' or message.content.lower() == 'whoa.':
                yield from client.send_message(message.channel, 'Hey guys.')
            elif message.content.lower() == 'hey guys' or message.content.lower() == 'hey guys':
                yield from client.send_message(message.channel, 'Welcome to EB Games.')
            elif ('call of duty' in message.content.lower() or 'advanced warfare' in message.content.lower() or 'xbox one' in message.content.lower()):
                yield from client.send_message(message.channel, 'Copy that.')

@base.postcommand
def wow(message, client, *args, **kwargs):
    if random.randint(0, 9000) == 1366:
        if message.author.id != client.user.id:
            if message.content.lower() == 'wow' or message.content.lower() == 'wow.':
                yield from client.send_message(message.channel, 'Ethan, great moves. Keep it up. I\'m proud of you.')
