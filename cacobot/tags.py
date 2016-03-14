import json
import random
import urllib.request
import urllib.parse
import re

import discord

import cacobot.base as base

# json to load tags and config
# random to generate random emojis for orphan
# urllibs to post configs to pastebin
# re to find mentions

mention_syntax = re.compile(r'(<@([0-9]*?)>)')

@base.cacofunc
async def tag(message, client):
    '''
    **{0}tag** <create | delete | edit | rename | gift | list | *tag id*> [mine | *content* | *tag id*] [*content* | *new id* | *new content* | *mention*]
    Allows you to manage tags.
    **{0}tag create [*id*] [*content*]** will create a new tag with the id [id] and content [content].
    **{0}tag delete [*id*]** will let you delete a tag, as long as you own it.
    **{0}tag edit [*id*] [*new content*]** will change [*id*]'s content to [*new content*].
    **{0}tag rename [*id*] [*new id*]** will change a tag's id to [*new id*].
    **{0}tag gift [*id*] [*mention*]** will change the owner of the tag to [*mention*].
    **{0}tag orphan [*id*]** will orphan a tag, allowing anyone to become the owner.
    **{0}tag claim [*id*]** lets you claim a tag that has been orphaned.
    **{0}tag list** will DM you all of the tags created in this server.
    **{0}tag list all** will list ALL of the tags CacoBot has.
    **{0}tag list mine** will DM you all of the tags you personally own.
    **{0}tag list orphaned** will DM you all of the tags that have no owner.
    **{0}tag [*id*]** will puke the tag with the id [*id*].
    **{0}tag [*id*] [*content*]** will implicitly create a tag if it can't find one.
    *Example: `{0}tag create gitgud http://i.imgur.com/Y3AZ1uX.jpg`*
    *(If a bot in your server already has tags, use their implementation, please. You can still use our tags, though. We have the AOE II taunts under tags 01-30! Try `{0}tag 08` and see what we mean!)*
    '''

    # Each tag has three objects: ['tag'], ['server'] and ['owner']. ['tag'] is the tag
    # itself, ['owner'] is the id of the tag's owner, and ['server] is the ID of the
    # server the tag was created on. ['owner'] and ['server'] can be "None" (as a
    # string) if nobody owns it.

    # I think Discord strips server-side already, but you can never be too careful.
    try:
        # Load tags
        with open('configs/tags.json') as z:
            tags = json.load(z)

        cmd = message.content.split()[1] #[0] is ".tag"

        # These commands all use the same params
        if cmd in ['create', 'delete', 'gift', 'list', 'edit', 'orphan', 'claim']:

            p = message.content.split(None, 1)[1]

            while mention_syntax.search(p):
                p = p.replace(mention_syntax.search(p).group(1), '@' + discord.utils.get(message.server.members, id=mention_syntax.search(p).group(2)).name)

            params = p.split(None, 3)

            if cmd == 'create':
                if params[1] in tags:
                    await client.send_message(message.channel, ':no_entry_sign: The tag {} already exists. (It looks like this:)\n{}'.format(params[1], tags[params[1]]['tag']))
                else:
                    tags[params[1]] = {
                        'tag': params[2],
                        'owner': message.author.id
                    }
                    if not message.channel.is_private:
                        tags[params[1]]['server'] = message.server.id
                    else:
                        tags[params[1]]['server'] = 'None'
                    await client.send_message(message.channel, ':heavy_check_mark: Successfully created the tag `{}`.'.format(params[1]))

            elif cmd == 'delete':
                if params[1] in tags:
                    if message.author.id == tags[params[1]]['owner'] or (not message.channel.is_private and message.channel.permissions_for(message.author).manage_roles and message.server.id == tags[params[1]]['server']):
                        tags.pop(params[1])
                        await client.send_message(message.channel, ':heavy_check_mark: Successfully deleted the tag `{}`.'.format(params[1]))
                    else:
                        if tags[params[1]]['owner'] == 'None':
                            await client.send_message(message.channel, '{} This tag is **orphaned**. You can claim ownership with `.tag claim {}`'.format(random.choice([':boy:', ':girl:']), params[1]))
                        else:
                            await client.send_message(message.channel, ':no_entry_sign: You do not have permission to modify this tag.')
                else:
                    await client.send_message(message.channel, ':no_entry_sign: The tag `{}` could not be found.'.format(params[1]))

            elif cmd == 'gift':
                if params[1] in tags:
                    if tags[params[1]]['owner'] == message.author.id:
                        if message.mentions:
                            tags[params[1]]['owner'] = message.mentions[0].id
                            await client.send_message(message.channel, ':heart: {}: {} has gifted you the tag `{}`.'.format(message.mentions[0].mention, message.author.mention, params[1]))
                        else:
                            await client.send_message(message.channel, ':no_entry_sign: You did not specify a user to gift the tag to.')
                    else:
                        if tags[params[1]]['owner'] == 'None':
                            await client.send_message(message.channel, '{} This tag is **orphaned**. You can claim ownership with `.tag claim {}`'.format(random.choice([':boy:', ':girl:']), params[1]))
                        else:
                            await client.send_message(message.channel, ':no_entry_sign: You do not have permission to modify this tag.')
                else:
                    await client.send_message(message.channel, ':no_entry_sign: The tag `{}` could not be found.'.format(params[1]))

            elif cmd == 'list':
                if len(params) > 1:
                    if params[1] == 'mine':
                        lst = 'Retrieving tags owned by {}:\n\n'.format(message.author.name)

                        dect = {}
                        for x in [x for x in tags if tags[x]['owner'] == message.author.id]:
                            serv = discord.utils.find(lambda y: y.id == tags[x]['server'], client.servers)
                            if serv == None:
                                if 'Direct Messages' in dect:
                                    dect['Direct Messages'].append(x)
                                else:
                                    dect['Direct Messages'] = [x]
                            else:
                                if serv.name in dect:
                                    dect[serv.name].append(x)
                                else:
                                    dect[serv.name] = [x]

                        for x in dect:
                            lst += '{}\n=======================\n'.format(x)
                            for y in dect[x]:
                                lst += y + ' '
                            lst += '\n\n'

                        values = {
                          'api_dev_key' : base.config['pastebin_key'],
                          'api_option' : 'paste',
                          'api_paste_code' : lst,
                          'api_paste_private' : '1',
                          'api_paste_expire_date' : '10M'
                        }

                        z = urllib.parse.urlencode(values)
                        z = z.encode('utf-8') # data should be bytes
                        req = urllib.request.Request('http://pastebin.com/api/api_post.php', z)

                        with urllib.request.urlopen(req) as response:
                            api_response = response.read().decode("utf-8")

                        await client.send_message(message.author, api_response)
                    elif params[1] == 'orphaned':
                        lst = 'These tags have no owner and can be claimed:\n\n'

                        for x in [x for x in tags if tags[x]['owner'] == 'None']:
                            lst += x + ' '

                        values = {
                          'api_dev_key' : base.config['pastebin_key'],
                          'api_option' : 'paste',
                          'api_paste_code' : lst,
                          'api_paste_private' : '1',
                          'api_paste_expire_date' : '10M'
                        }

                        z = urllib.parse.urlencode(values)
                        z = z.encode('utf-8') # data should be bytes
                        req = urllib.request.Request('http://pastebin.com/api/api_post.php', z)

                        with urllib.request.urlopen(req) as response:
                            api_response = response.read().decode("utf-8")

                        await client.send_message(message.author, api_response)
                    elif params[1] == 'all':
                        lst = 'Here\'s a list of all the tags I know.\n\n'

                        mv = 0
                        orph = 0

                        dect = {}
                        for x in tags:
                            if tags[x]['owner'] == 'None':
                                if 'Orphaned' in dect:
                                    dect['Orphaned'].append(x)
                                else:
                                    dect['Orphaned'] = [x]
                            else:
                                if tags[x]['server'] == 'None':
                                    if 'Direct Messages' in dect:
                                        dect['Direct Messages'].append(x)
                                    else:
                                        dect['Direct Messages'] = [x]
                                else:
                                    if discord.utils.find(lambda y: y.id == tags[x]['server'], client.servers):
                                        if discord.utils.find(lambda y: y.id == tags[x]['server'], client.servers).name in dect:
                                            dect[discord.utils.find(lambda y: y.id == tags[x]['server'], client.servers).name].append(x)
                                        else:
                                            dect[discord.utils.find(lambda y: y.id == tags[x]['server'], client.servers).name] = [x]
                                    else:
                                        mv += 1
                                        ownerAround = False
                                        for z in client.servers:
                                            if [y for y in z.members if y.id == tags[x]['owner']]:
                                                ownerAround = True
                                        tags[x]['server'] = 'None'
                                        if not ownerAround:
                                            tags[x]['owner'] = 'None'
                                            orph += 1
                                            if 'Orphaned' in dect:
                                                dect['Orphaned'].append(x)
                                            else:
                                                dect['Orphaned'] = [x]

                        for x in dect:
                            lst += '{}\n=======================\n'.format(x)
                            for y in dect[x]:
                                lst += y + ' '
                            lst += '\n\n'

                        values = {
                            'api_dev_key' : base.config['pastebin_key'],
                            'api_option' : 'paste',
                            'api_paste_code' : lst,
                            'api_paste_private' : '1',
                            'api_paste_expire_date' : '10M'
                        }

                        z = urllib.parse.urlencode(values)
                        z = z.encode('utf-8') # data should be bytes
                        req = urllib.request.Request('http://pastebin.com/api/api_post.php', z)

                        with urllib.request.urlopen(req) as response:
                            api_response = response.read().decode("utf-8")

                        if mv:
                            if orph:
                                await client.send_message(message.channel, 'I automatically moved {} tags into DMs. Of them, {} were orphaned.'.format(mv, orph))
                            else:
                                await client.send_message(message.channel, 'I automatically moved {} tags into DMs.'.format(mv))
                        await client.send_message(message.author, api_response)
                else:
                    if message.channel.is_private:
                        lst = 'Here\'s a list of all the tags created in direct messages with me.\n\n'
                    else:
                        lst = 'Here\'s a list of all the tags created in the {} server.\n\n'.format(message.server.name)
                    if not message.channel.is_private:
                        for x in [x for x in tags if tags[x]['server'] == message.server.id]:
                            lst += x + ', '
                    else:
                        for x in [x for x in tags if tags[x]['server'] == 'None']:
                            lst += x + ', '
                    lst = lst[:-2]

                    values = {
                        'api_dev_key' : base.config['pastebin_key'],
                        'api_option' : 'paste',
                        'api_paste_code' : lst,
                        'api_paste_private' : '1',
                        'api_paste_expire_date' : '10M'
                    }

                    z = urllib.parse.urlencode(values)
                    z = z.encode('utf-8') # data should be bytes
                    req = urllib.request.Request('http://pastebin.com/api/api_post.php', z)

                    with urllib.request.urlopen(req) as response:
                        api_response = response.read().decode("utf-8")

                    await client.send_message(message.author, api_response)

            elif cmd == 'edit':
                if params[1] in tags:
                    if tags[params[1]]['owner'] == message.author.id:
                        tags[params[1]]['tag'] = params[2]
                        await client.send_message(message.channel, ':heavy_check_mark: Successfully edited the tag `{}`.'.format(params[1]))
                    else:
                        if tags[params[1]]['owner'] == 'None':
                            await client.send_message(message.channel, '{} This tag is **orphaned**. You can claim ownership with `.tag claim {}`'.format(random.choice([':boy:', ':girl:']), params[1]))
                        else:
                            await client.send_message(message.channel, ':no_entry_sign: You do not have permission to modify this tag.')
                else:
                    await client.send_message(message.channel, ':no_entry_sign: The tag `{}` could not be found.'.format(params[1]))

            elif cmd == 'orphan':
                if params[1] in tags:
                    if tags[params[1]]['owner'] == message.author.id:
                        tags[params[1]]['owner'] = 'None'
                        tags[params[1]]['server'] = 'None'
                        await client.send_message(message.channel, '{} You have orphaned the tag `{}`.'.format(random.choice([':boy:', ':girl:']), params[1]))
                    else:
                        if tags[params[1]]['owner'] == 'None':
                            await client.send_message(message.channel, '{} This tag is **orphaned**. You can claim ownership with `.tag claim {}`'.format(random.choice([':boy:', ':girl:']), params[1]))
                        else:
                            await client.send_message(message.channel, ':no_entry_sign: You do not have permission to modify this tag.')
                else:
                    await client.send_message(message.channel, ':no_entry_sign: The tag `{}` could not be found.'.format(params[1]))

            elif cmd == 'claim':
                if params[1] in tags:
                    if tags[params[1]]['owner'] == 'None':
                        tags[params[1]]['owner'] = message.author.id
                        if not message.channel.is_private:
                            tags[params[1]]['server'] = message.server.id
                        else:
                            tags[params[1]]['server'] = 'None'
                        await client.send_message(message.channel, ':children_crossing: You have claimed the tag `{}`.'.format(params[1]))
                    else:
                        await client.send_message(message.channel, ':no_entry_sign: This tag is owned by <@{}>.'.format(tags[params[1]]['owner']))
                else:
                    await client.send_message(message.channel, ':no_entry_sign: The tag `{}` could not be found.'.format(params[1]))

        elif cmd == 'rename':
            p = message.content.split(None, 1)[1]

            while mention_syntax.search(p):
                p = p.replace(mention_syntax.search(p).group(1), '@' + discord.utils.get(message.server.members, id=mention_syntax.search(p).group(2)).name)

            params = p.split()

            if params[1] in tags:
                if tags[params[1]]['owner'] == message.author.id:
                    tags[params[2]] = tags.pop(params[1])
                    await client.send_message(message.channel, ':heavy_check_mark: Successfully renamed the tag `{}` to `{}`.'.format(params[1], params[2]))
                else:
                    if tags[params[1]]['owner'] == 'None':
                        await client.send_message(message.channel, '{} This tag is **orphaned**. You can claim ownership with `.tag claim {}`'.format(random.choice([':boy:', ':girl:']), params[1]))
                    else:
                        await client.send_message(message.channel, ':no_entry_sign: You do not have permission to modify this tag.')
            else:
                await client.send_message(message.channel, ':no_entry_sign: The tag `{}` could not be found.'.format(params[1]))

        else:
            p = message.content.split(None, 1)[1]

            while mention_syntax.search(p):
                p = p.replace(mention_syntax.search(p).group(1), '@' + discord.utils.get(message.server.members, id=mention_syntax.search(p).group(2)).name)

            params = p.split(None, 1)


            if cmd in tags:
                await client.send_message(message.channel, tags[cmd]['tag'])
            else:
                if len(params) > 1:
                    tags[params[0]] = {
                        'tag': params[1],
                        'owner': message.author.id
                    }
                    if not message.channel.is_private:
                        tags[params[0]]['server'] = message.server.id
                    else:
                        tags[params[0]]['server'] = 'None'
                    await client.send_message(message.channel, ':heavy_check_mark: Successfully created the tag `{}`.'.format(params[0]))

                else:
                    await client.send_message(message.channel, ':no_entry_sign: The tag {} could not be found.'.format(cmd))

        #re-save tags.json
        with open('configs/tags.json', 'w') as file:
            json.dump(tags, file, indent=4)
    except IndexError:
        await client.send_message(message.channel, "If you need help on using this command, call `{}help tag`!".format(
            base.config['invoker']
            ))
