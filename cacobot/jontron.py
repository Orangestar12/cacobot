import re
import random
import asyncio
import json
import cacobot.base as base

with open('configs/config.json') as data:
    config = json.load(data)

whitelist = [
    ('99293578949316608', '142417518118699008'),
    ('120330239996854274', '120331931735949313'),
    ('120205773425868804', '139862570130472961'),
    ('128043020418285568', '128043174647169024'),
    ('99293578949316608', '147832765910482945'),
    ('149167686159564800', '150638634591191040'),
    ('148514071589683200', '150495955857178624')
]

@base.postcommand
async def koolaid(message, client):
    if (message.server.id, message.channel.id) in whitelist:
        if re.match(r'.*thought i misplaced it[?!.]*$', message.content.lower().replace('*', '')) and\
                message.author.id != client.user.id:
            # Change Avatar
            with open('ethan/ethan.png', 'rb') as wow_ethan:
                await client.edit_profile(config['password'], avatar=wow_ethan.read())

            # comedic timing
            await asyncio.sleep(5)

            # This is a faster way of doing "if random.choice([True, False])"
            if bool(random.getrandbits(1)):
                await client.send_message(
                    message.channel,
                    '\\*Jiggles door handle.\\*'
                )
                await asyncio.sleep(1)

            await client.send_message(
                message.channel,
                '\\*Opens door.\\*'
                )
            await asyncio.sleep(1)
            await client.send_message(
                message.channel,
                'Hey dude, what\'s up?'
            )
            await asyncio.sleep(1)

            if bool(random.getrandbits(1)):
                await client.send_message(
                    message.channel,
                    'Yeah.'
                )
                await asyncio.sleep(1)

            await client.send_message(
                message.channel,
                'Here\'s your game, buddy.'
            )
            await asyncio.sleep(1)
            await client.send_message(
                message.channel,
                'Here\'s your Kool-Aid game here man.'
            )
            await asyncio.sleep(1)

            if bool(random.getrandbits(1)):
                await client.send_message(
                    message.channel,
                    'Here you go.'
                )
                await asyncio.sleep(1)

            await client.send_message(
                message.channel,
                'I\'m the Kool-Aid guy. Yeah.'
            )

            if bool(random.getrandbits(1)):
                await client.send_message(
                    message.channel,
                    'There it is.'
                )

            def ok(message):
                return re.match(r'^(oh?(,|\.*)? )?thanks[.]*$', message.content.lower())

            msg = await client.wait_for_message(
                timeout=60, author=message.author,
                channel=message.channel, check=ok)

            if msg:
                await client.send_message(
                    message.channel,
                    'No prob, buddy. Hey, didja want some Kool-Aid before I left here?'
                )

                def oktwo(message):
                    return re.match(
                        r'^(yeah|yes|sure)((,|\.*) ok(ay)?[.!]*)?$',
                        message.content.lower()
                        )

                msgtwo = await client.wait_for_message(
                    timeout=60, author=message.author,
                    channel=message.channel, check=oktwo)

                if msgtwo:
                    if bool(random.getrandbits(1)):
                        await client.send_message(
                            message.channel,
                            'You wanna try a little Kool-Aid?'
                        )
                        await asyncio.sleep(1)

                    await client.send_message(
                        message.channel,
                        '*Punch me in the liver, dude.*'
                    )

                    def okthree(message):
                        return re.match(r'^\**what[?!.]*\**$', message.content.lower())

                    msgthree = await client.wait_for_message(
                        timeout=60, author=message.author,
                        channel=message.channel, check=okthree)

                    if msgthree:
                        await client.send_message(
                            message.channel,
                            '*Punch me in the* ***FUCKING LIVER.***'
                        )

                        finalmsg = await client.wait_for_message(
                            timeout=60, author=message.author,
                            channel=message.channel)

                        if finalmsg:
                            await client.send_file(message.channel, 'ethan/i.png')
                            await client.send_file(message.channel, 'ethan/said.png')
                            await client.send_file(message.channel, 'ethan/just.png')
                            await client.send_file(message.channel, 'ethan/once.png')
                            await client.send_message(
                                message.channel,
                                '...Ugh... Man! I said just once, man!'
                                )

            with open('avatar.jpg', 'rb') as avatar:
                await client.edit_profile(config['password'], avatar=avatar.read())
