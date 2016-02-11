import re
import random
import asyncio
import json
import cacobot.base as base

with open('configs/config.json') as data:
    config = json.load(data)

@base.postcommand
def koolaid(message, client):
    if re.match(r'.*thought i misplaced it[?!.]*$', message.content.lower()) and\
            message.author.id != client.user.id:
        # Change Avatar
        with open('ethan/ethan.png', 'rb') as wow_ethan:
            yield from client.edit_profile(config['password'], avatar=wow_ethan.read())

        # comedic timing
        yield from asyncio.sleep(15)

        # This is a faster way of doing "if random.choice([True, False])"
        if bool(random.getrandbits(1)):
            yield from client.send_message(
                message.channel,
                '\\*Jiggles door handle.\\*'
            )
            yield from asyncio.sleep(2)

        yield from client.send_message(
            message.channel,
            '\\*Opens door.\\*'
            )
        yield from asyncio.sleep(4)
        yield from client.send_message(
            message.channel,
            'Hey dude, what\'s up?'
        )
        yield from asyncio.sleep(5)

        if bool(random.getrandbits(1)):
            yield from client.send_message(
                message.channel,
                'Yeah.'
            )
            yield from asyncio.sleep(3)

        yield from client.send_message(
            message.channel,
            'Here\'s your game, buddy.'
        )
        yield from asyncio.sleep(2)
        yield from client.send_message(
            message.channel,
            'Here\'s your Kool-Aid game here man.'
        )
        yield from asyncio.sleep(2)

        if bool(random.getrandbits(1)):
            yield from client.send_message(
                message.channel,
                'Here you go.'
            )
            yield from asyncio.sleep(3)

        yield from client.send_message(
            message.channel,
            'I\'m the Kool-Aid guy. Yeah.'
        )

        if bool(random.getrandbits(1)):
            yield from asyncio.sleep(2)
            yield from client.send_message(
                message.channel,
                'There it is.'
            )

        def ok(message):
            return re.match(r'^(oh?(,|\.*)? )?thanks[.]*$', message.content.lower())

        msg = yield from client.wait_for_message(
            timeout=60, author=message.author,
            channel=message.channel, check=ok)

        if msg:
            yield from client.send_message(
                message.channel,
                'No prob, buddy. Hey, didja want some Kool-Aid before I left here?'
            )

            def oktwo(message):
                return re.match(
                    r'^(yeah|yes|sure)((,|\.*) ok(ay)?[.!]*)?$',
                    message.content.lower()
                    )

            msgtwo = yield from client.wait_for_message(
                timeout=60, author=message.author,
                channel=message.channel, check=oktwo)

            if msgtwo:
                if bool(random.getrandbits(1)):
                    yield from client.send_message(
                        message.channel,
                        'You wanna try a little Kool-Aid?'
                    )
                    yield from asyncio.sleep(3)

                yield from client.send_message(
                    message.channel,
                    '*Punch me in the liver, dude.*'
                )

                def okthree(message):
                    return re.match(r'^\**what[?!.]*\**$', message.content.lower())

                msgthree = yield from client.wait_for_message(
                    timeout=60, author=message.author,
                    channel=message.channel, check=okthree)

                if msgthree:
                    yield from client.send_message(
                        message.channel,
                        '*Punch me in the* ***FUCKING LIVER.***'
                    )

                    finalmsg = yield from client.wait_for_message(
                        timeout=60, author=message.author,
                        channel=message.channel)

                    if finalmsg:
                        yield from client.send_file(message.channel, 'ethan/i.png')
                        yield from asyncio.sleep(3)
                        yield from client.send_file(message.channel, 'ethan/said.png')
                        yield from asyncio.sleep(3)
                        yield from client.send_file(message.channel, 'ethan/just.png')
                        yield from asyncio.sleep(3)
                        yield from client.send_file(message.channel, 'ethan/once.png')
                        yield from asyncio.sleep(3)
                        yield from client.send_message(
                            message.channel,
                            '...Ugh... Man! I said just once, man!'
                            )

        with open('avatar.jpg', 'rb') as avatar:
            yield from client.edit_profile(config['password'], avatar=avatar.read())
