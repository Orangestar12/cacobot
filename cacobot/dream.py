import cacobot.base as base
import discord, re, json, random

# discord for channel management
# re for content stripping
# json for databases

everyperm = discord.Permissions.none()
everyperm.send_messages = True
ownerperm = discord.Permissions.none()
ownerperm.send_messages = True
ownerperm.manage_channels = True
ownerperm.manage_messages = True
ownerperm.manage_roles = True

@base.cacofunc
async def journal(message, client, *args, **kwargs):
    '''
    **.journal**
    *This command was created for the Dream Journals server.*
    Creates a new text channel that only you can post in, using your name as the title.
    **This command is only enabled if a moderator calls `.journal activate` first.**
    *Example: `.journal`*
    '''

    journals = []

    try:
        with open('configs/journals.json') as data:
            journals = json.load(data)
    except FileNotFoundError:
        with open('configs/journals.json', 'w') as data:
            data.write('[]')

    if message.content.strip()[len(base.config['invoker']):] == 'journal activate':
        if message.channel.permissions_for(message.author).manage_channels:
            journals.append(message.server.id)
            with open('configs/journals.json', 'w') as data:
                json.dump(journals, data, indent=4)
            await client.send_message(message.channel, ":+1: Users are now allowed to add journals to your server!")
        else:
            await client.send_message(message.channel, ":no_entry_sign: You are not allowed to manage text channels in this server.")
    else:
        if message.server.id in journals:
            weird = False
            channel_name = re.sub('[^A-Za-z0-9_-]', '-', message.author.name.lower()).strip('-_')
            if not channel_name:
                channel_name = []
                for x in range(10):
                    channel_name.append(random.choice('0123456789abcdefghijklmnopqrstuvwxyz'))
                channel_name = ''.join(channel_name)
                weird = True

            if message.channel.permissions_for(discord.utils.get(message.server.members, id=client.user.id)).manage_channels:
                newch = await client.create_channel(message.server, channel_name)
                await client.edit_channel_permissions(newch, message.server.default_role, deny=everyperm)
                await client.edit_channel_permissions(newch, message.author, allow=ownerperm)
                if weird:
                    await client.send_message(message.channel, ":warning: I had a lot of trouble trying to parse your name for your channel. Instead, I just gave you a random alphanumeric code! Your channel is {}. You should probably change the name by clicking the **⚙** next to your channel in the list.".format(newch.mention))
                else:
                    await client.send_message(message.channel, ":+1: I have successfully created a journal channel for you. Feel free to change it's name or modify the permissions on it by clicking the **⚙** next to your channel in the list.")
            else:
                await client.send_message(message.channel, ":no_entry_sign: I do not have the proper permissions to create a journal channel for you yet.")
        else:
            await client.send_message(
                message.channel,
                ":no_entry_sign: This server is disallowed from making Journals. If you would like to enable it, have a moderator call `{}journal activate`.".format(
                    base.config['invoker']
                    )
                )

journal.server = 'Dream Journals'
