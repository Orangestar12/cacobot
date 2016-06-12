# pylint: disable=W0106, R0101

import json # to load tags
import random # to generate random emojis for orphan
import inspect # to get docstrings
import urllib.request # to post configs to pastebin
import urllib.parse
import re # re to find mentions and strip tags of invalid chars

import discord

import cacobot.base as base

# Load tags
try:
    with open('configs/tags.json') as Z:
        tags = json.load(Z)
# Create tags if not found
except FileNotFoundError:
    with open('configs/tags.json', 'w') as Z:
        Z.write('{}')
        tags = {}

# mention_syntax is a useful regex that matches any mention of a person.
# i.e. <@88401933936640000> (which resolves to @Orangestar) would capture, and
# return the ID as the second capturing group (The mention itself is the first.)
# Includes # for discriminators now (It's a shitty fix but it works)
mention_syntax = re.compile(r'(<@([0-9#]*?)>)')

# limit is a regex that only includes alphanumeric characters, underscores, and
# dashes.
limit = re.compile(r'[^a-z0-9_-]')

async def sub(msg, message, client):
    '''
    Strips `msg` of nonalphanumeric characters, and returns it. Will also notify
    the user when this happens.
    '''
    x = limit.sub('', msg.lower())
    if msg != x:
        await client.send_message(
            message.channel,
            '*\u2139 {}: Your tag name was stripped to `{}`.*'.format(
                message.author.display_name,
                x
                )
            )
    return x

def pastebin(text):
    values = {
        'api_dev_key' : base.config['pastebin_key'],
        'api_option' : 'paste',
        'api_paste_code' : text,
        'api_paste_private' : '1',
        'api_paste_expire_date' : '10M'
        }

    z = urllib.parse.urlencode(values)
    z = z.encode('utf-8') # data should be bytes
    req = urllib.request.Request('http://pastebin.com/api/api_post.php', z)

    with urllib.request.urlopen(req) as response:
        api_response = response.read().decode("utf-8")

    return api_response

def valid(msg):
    '''
    Returns `True`, so long as `msg` does not contain a user mention or
    "@everyone"
    '''
    if mention_syntax.search(msg):
        return False
    if '@everyone' in msg:
        return False
    if '@here' in msg:
        return False
    return True

async def totalparams(name, req, num, message, client):
    '''
    Returns `False` and notifies the user if `num` is less than `req`. `name` is
    the phrase `totalparams` will respond with.
    '''
    if num < req:
        await client.send_message(
            message.channel,
            '\U0001F6AB {0}: You must provide at least 4 parameters for `{1}`. Use `{2}tag help {1}` for more information.'.format(
                message.author.display_name,
                name,
                base.config['invoker']
                )
            )
        return False
    return True

async def sendorphan(existing, message, client):
    if tags[existing]['owner'] == 'None':
        await client.send_message(
            message.channel,
            '{} {}: This tag is **orphaned**. You can claim ownership with `{}tag claim {}`'.format(
                random.choice(
                    [
                        '\U0001F466', # :boy:
                        '\U0001F467'  # :girl:
                    ]
                    ),
                message.author.display_name,
                base.config['invoker'],
                existing
                )
            )
        return True

def updatetags():
    '''re-saves tags.json'''
    with open('configs/tags.json', 'w') as z:
        json.dump(tags, z, indent=4)

# This is a list of commands `tag` requires, so that users can't `create` (or
# `rename`) a tag with these as names.
reserved = {'create', 'delete', 'edit', 'rename', 'gift', 'list', 'move', 'add', 'remove', 'owner', 'recall', 'claim', 'orphan'}

@base.cacofunc
async def reloadtags(message, client):
    '''
    ***{0}reloadtags***
    Re-reads the contents of `tags.json` and applies it as the current tag list.
    *This is a debug command. Only the bot owner can use it.*
    *Example: `{0}reloadtags`*
    '''
    if message.author.id == base.config['owner_id']:
        global tags
        with open('configs/tags.json') as z:
            tags = json.load(z)
        await client.send_message(message.channel, '✔ {}: Successfully reloaded `tags.json`.'.format(
            message.author.display_name
            ))
        return
    await client.send_message(message.channel, '\U0001F6AB {}: You are not allowed to use this command.'.format(
        message.author.display_name
        ))
reloadtags.server = 'hidden'

@base.cacofunc
async def tag(message, client):
    '''
    **{0}tag** <options> <tag id>, **{0}tag** <tag id>
    Allows you to store and recall strings inside CacoBot.
    **Options:**
    `create`, `delete`, `edit`, `rename`, `gift`, `list`, ~~`claim`, `orphan`, `move`, `owner`,~~ `recall`
    Use `{0}tag help option` for more information on an option.
    '''

    # Each tag has three entries: ['tag'], ['server'] and ['owner']. ['tag'] is the tag
    # itself, ['owner'] is the id of the tag's owner, and ['server] is the ID of the
    # server the tag was created on. ['owner'] and ['server'] can be "None" (as a
    # string) if nobody owns it.

    # make sure tag is valid before proceeding
    if not message.content.startswith('{}tag recall'.format(base.config['invoker'])) and not valid(message.content):
        await client.send_message(
            message.channel,
            '\U0001F6AB {}: You are not allowed to provide mentions, "@\u2060everyone", or "@\u2020here" in your messages.'.format(
                message.author.display_name
                )
            )
        return

    params = message.content.split()
    # we can always go back and `split` message.content selectively if we need
    # a string or something.

    # just `.tag`
    if len(params) == 1:
        await client.send_message(
            message.channel,
            '\U0001F6AB {0}: You did not specify any options. Please use `{1}help tag` or `{1}tag help option` for more information.'.format(
                message.author.display_name,
                base.config['invoker']
                )
            )
        return

    # because people fuck this up too much
    if params[1] in ['add', 'remove']:
        await client.send_message(
            message.channel,
            '{}: `{}tag` uses `create` and `delete` instead of `add` and `remove`.'.format(
                message.author.display_name,
                base.config['invoker']
                )
            )
        return

    # most of these params[x] == 'phrase' entries should be self-explanatory
    # so i hope nobody needed comments here

    if params[1] == 'help':

        # Response was valid
        if len(params) > 2 and params[2] in reserved:

            # Sure, let's do it here too
            if params[2] in ['add', 'remove']:
                await client.send_message(
                    message.channel,
                    '{}: `{}tag` uses `create` and `delete`, not `add` and `remove`.'.format(
                        message.author.display_name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'create':
                await client.send_message(
                    message.channel,
                    '{}: `{}tag create <tag name> <tag content>`\nCreates a new tag with the name <tag name> and the content <tag content>. Tag names are limited to alphanumeric characters (A-Z and 0-9) and are case sensitive. Tags that contain a user mention, "@\u2060everyone", or "@\u2020here" are automatically rejected at face value.'.format(
                        message.author.display_name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'delete':
                await client.send_message(
                    message.channel,
                    '{}: `{}tag delete <tag name>`\nDeletes the tag <tag name>, so long as you are the owner.'.format(
                        message.author.display_name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'edit':
                await client.send_message(
                    message.channel,
                    '{}: `{}tag edit <tag name> <tag content>`\nReplaces the contents of the tag <tag name>, so long as you are the owner.'.format(
                        message.author.display_name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'rename':
                await client.send_message(
                    message.channel,
                    '{}: `{}tag rename <old id> <new id>`\nChanges the tag id of <old id> to <new id>, so long as you are the owner.'.format(
                        message.author.display_name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'list':
                await client.send_message(
                    message.channel,
                    '{}: `{}tag list [all]`\nSends you a list of all tags you own. Send `.tag list all` to see every tag.'.format(
                        message.author.display_name,
                        base.config['invoker']
                        )
                    )
                return

            if params[2] == 'recall':
                await client.send_message(
                    message.channel,
                    '{}: `{}tag recall <tag name>`\nCalls the tag <tag name>, and informs you why it cannot be used in standard channels. Input is not stripped or substituted for this command.\n*This option only works in Direct Messages.*'.format(
                        message.author.display_name,
                        base.config['invoker']
                        )
                    )
                return

            # UGH FUCK
            await client.send_message(
                message.channel,
                '{}: Sorry, I don\'t have a help entry for this yet. I wanted to get the command finished and rolled out before I did the fluff like this.'.format(
                    message.author.display_name
                    )
                )
            return

        # Response was invalid, but not empty
        elif len(params) > 2:
            await client.send_message(
                message.channel,
                '{}: That is not a valid option for `{}tag`.'.format(
                    message.author.display_name,
                    base.config['invoker']
                    )
                )
            return

        # Empty response: dump help docstring
        else:
            await client.send_message(
                message.channel,
                inspect.getdoc(tag).format(
                    base.config['invoker']
                    )
                )
            return
    # end help

    # A lot of this stuff gets repeated further down the code so pay attention
    if params[1] == 'create':
        # stop if not enough parameters
        if not await totalparams('create', 4, len(params), message, client):
            return

        # strip alphanumeric chars
        params[2] = await sub(params[2], message, client)

        # tag name is reserved
        if params[2] in reserved:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: That string is reserved.'.format(
                    message.author.display_name
                    )
                )
            return

        # tag name already exists:
        if params[2] in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: The tag `{}` already exists. (It looks like this:)\n{}'.format(
                    message.author.display_name,
                    params[2],
                    tags[params[2]]['tag']
                    )
                )
            return

        # create tag

        tags[params[2]] = {
            'tag': message.content.split(None, 3)[3],
            'owner': message.author.id
        }

        # determine server
        if message.channel.is_private:
            tags[params[2]]['server'] = 'None'
        else:
            tags[params[2]]['server'] = message.server.id

        await client.send_message(
            message.channel,
            '✔ {}: Successfully created the tag `{}`.'.format(
                message.author.display_name,
                params[2]
                )
            )

        updatetags()
        return
    # end create

    if params[1] == 'delete':
        if not await totalparams('delete', 3, len(params), message, client):
            return

        params[2] = await sub(params[2], message, client)

        # tag not found
        if params[2] not in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: The tag `{}` does not exist.'.format(
                    message.author,
                    params[2]
                    )
                )
            return

        # user owns tag: delete
        if message.author.id == tags[params[2]]['owner']:
            tags.pop(params[2])
            await client.send_message(
                message.channel,
                '✔ {}: Successfully deleted the tag `{}`.'.format(
                    message.author.display_name,
                    params[2]
                    )
                )
            updatetags()
            return

        # user owns bot: delete
        if message.author.id == base.config['owner_id']:
            tagid = tags[params[2]]['owner']
            tags.pop(params[2])
            await client.send_message(
                message.channel,
                '✔ {}: Successfully deleted the tag `{}`. (Owner ID: {})'.format(
                    message.author.display_name,
                    params[2],
                    tagid
                    )
                )
            updatetags()
            return

        # server owns tag & invoker is admin: delete
        if not message.channel.is_private and \
         message.server.id == tags[params[2]]['server'] and \
         message.channel.permissions_for(message.author).manage_roles:
            tags.pop(params[2])
            await client.send_message(
                message.channel,
                '✔ {}: Successfully deleted the tag `{}`.'.format(
                    message.author.display_name,
                    params[2]
                    )
                )
            updatetags()
            return

        # tag is orphaned: notify user
        if await sendorphan(params[2], message, client):
            return

        await client.send_message(
            message.channel,
            '\U0001F6AB {}: You do not have permission to modify this tag.'.format(
                message.author.display_name
                )
            )
        return
    # end delete

    if params[1] == 'edit':
        if not await totalparams('edit', 4, len(params), message, client):
            return

        params[2] = await sub(params[2], message, client)

        if params[2] not in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: The tag `{}` does not exist.'.format(
                    message.author,
                    params[2]
                    )
                )
            return

        if message.author.id == tags[params[2]]['owner'] or \
         message.channel.permissions_for(message.author).manage_roles:
            tags[params[2]]['tag'] = message.content.split(None, 3)[3]
            updatetags()
            await client.send_message(
                message.channel,
                '✔ {}: Successfully updated the tag `{}`.'.format(
                    message.author.display_name,
                    params[2]
                    )
                )
            return

        await client.send_message(
            message.channel,
            '\U0001F6AB {}: You do not have permission to modify this tag.'.format(
                message.author.display_name
                )
            )
        return
    # end edit

    if params[1] == 'rename':
        if not await totalparams('rename', 4, len(params), message, client):
            return

        if params[2] not in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: That tag does not exist.\n*For now, `rename` requires exact case. Double-check your typing.*'.format(
                    message.author.display_name
                    )
                )
            return

        if message.author.id != tags[params[2]]['owner']:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: You do not have permission to modify this tag.'.format(
                    message.author.display_name
                    )
                )
            return

        params[3] == await sub(params[3], message, client)

        if params[3] in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: A tag already exists with the name {}.'.format(
                    message.author.display_name,
                    params[3]
                    )
                )
            return

        tags[params[3]] = tags[params[2]]
        tags.pop(params[2])
        updatetags()
        await client.send_message(
            message.channel,
            '✔ {}: Successfully renamed that tag to `{}`.'.format(
                message.author.display_name,
                params[3]
                )
            )
        return

    # end rename

    if params[1] == 'list':
        selection = None
        mine = True

        if len(params) > 2:
            if params[2] == 'mine':
                await client.send_message(
                    message.channel,
                    '\U0001F6AB {}: The syntax for this command has changed. `.tag list` will get your tags and orphaned tags. `.tag list all` will get all tags.'.format(
                        message.author.display_name
                        )
                    )
                return

            if params[2] == 'orphaned':
                await client.send_message(
                    message.channel,
                    '\U0001F6AB {}: The syntax for this command has changed. `.tag list` will get your tags and orphaned tags. `.tag list all` will get all tags.'.format(
                        message.author.display_name
                        )
                    )
                return

            if params[2] == 'all':
                selection = tags
                mine = None

        if not selection:
            selection = [x for x in tags if tags[x]['owner'] == message.author.id]

        dms = 0 # number of tags moved to dms
        orphans = 0 # number of tags orphaned

        dect = {}
        for x in selection:

            # no server: tag was made in DMs or is orphaned
            if tags[x]['server'] == 'None':

                # no owner: tag was orphaned
                if tags[x]['owner'] == 'None':
                    if 'Orphaned' in dect:
                        dect['Orphaned'].append(x)
                    else:
                        dect['Orphaned'] = [x]

                else:
                    if 'Direct Messages' in dect:
                        dect['Direct Messages'].append(x)
                    else:
                        dect['Direct Messages'] = [x]

            else:
                # find server to get it's name (we only store ID)
                serv = discord.utils.get(client.servers, id=tags[x]['server'])
                if serv is None:
                    # Caco was kicked from that server: DM the tag.
                    tags[x]['server'] = 'None'

                    dms += 1

                    # see if we can find that user: if he's still using
                    # the bot, that means we can just move the tag to DMs.
                    if discord.utils.get(client.get_all_members(), id=tags[x]['owner']) is None:
                        # The user isn't using Caco anymore: orphan the tag.
                        tags[x]['owner'] = 'None'
                        orphans += 1

                else:
                    if serv.name in dect:
                        dect[serv.name].append(x)
                    else:
                        dect[serv.name] = [x]

        # Construct string from Dictionary
        msg = ''

        if mine:
            msg = 'The following tags are owned by you:\n\n'

        for x in dect:
            msg += '{}\n=======================\n{}\n\n'.format(x, ' '.join(dect[x]))

        if mine:
            msg += 'In addition, the following tags are orphaned and can be claimed by anyone:\n\n{}'.format(
                ' '.join([x for x in tags if tags[x]['owner'] == 'None'])
                )

        # paste url to pastebin
        url = pastebin(msg)

        if dms:
            if orphans:
                await client.send_message(
                    message.channel,
                    '\u2139 {}: I automatically moved {} tags into DMs. Of those, {} tags were orphaned.'.format(
                        message.author.display_name,
                        dms,
                        orphans
                        )
                    )
            else:
                await client.send_message(
                    message.channel,
                    '\u2139 {}: I automatically moved {} tags into DMs.'.format(
                        message.author.display_name,
                        dms
                        )
                    )

        await client.send_message(message.author, url)
        return
    # end list

    if params[1] == 'gift':
        if not await totalparams('gift', 4, len(params), message, client):
            return

        params[2] == await sub(params[2], message, client)

        if params[2] not in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: I could not find a tag with that name.'.format(
                    message.author.display_name
                    )
                )
            return

        if tags[params[2]]['owner'] != message.author.id:
            if await sendorphan(params[2], message, client):
                return

            await client.send_message(
                message.channel,
                '\U0001F6AB {}: You do not have permission to modify this tag.'.format(
                    message.author.display_name
                    )
                )
            return

        member = None

        # user mentioned member: just take it
        if message.mentions:
            member = message.mentions[0]
        else:
            # user typed member name: convert to member
            name = message.content.split(None, 3)[3]
            members = [x for x in message.server.members if x.name == name]

            # no users with that name found
            if not members:
                await client.send_message(message.channel, '\U0001F6AB {}: I couldn\'t find a user by that name. Please either provide a mention for the member you would like to gift a tag to, or provide the user\'s whole name, case-sensitive.'.format(
                    message.author.display_name
                    ))
                return

            # multiple users with that name found
            if len(members) > 1:

                # build list of users with entries like: "1. Username#1234"
                # 1234 is discriminator
                msg = ''
                for i, x in enumerate(members):
                    msg += '\n{}: {}#{}'.format(i, x.name, x.discriminator)
                await client.send_message(message.channel, '\u2139 {}: I found multiple members with that name. Please type the number of the user with the correct discriminator:{}'.format(
                    message.author.display_name,
                    msg
                    ))

                # verify sucessful response
                cont = False
                while not cont:
                    response = await client.wait_for_message(channel=message.channel, author=message.author, timeout=30)

                    # no message after 30 seconds: timeout
                    if not response:
                        await client.send_message(message.channel, '\U0001F6AB {}: You have taken too long to provide an answer. Please try again later.'.format(
                            message.author.display_name
                            ))
                        return

                    try:
                        # convert response to int and select member based on int
                        p = int(response)

                        # int out of range
                        if p > len(members) or p < 1:
                            await client.send_message(message.channel, '\u2139 {}: You must provide a number between 1 or {}'.format(
                                message.author.display_name,
                                len(members)
                                ))

                        else:
                            member = members[p-1]
                            cont = True

                    except ValueError:
                        # don't say anything on ValueError since dude might be chatting
                        pass
            else:
                member = members[0]

        # catch obscure error
        if not member:
            await client.send_message(message.channel, '\U0001F6AB {}: **An unexpected error occurred:** No member object was assigned. Please try again.'.format(
                message.author.display_name
                ))

        # tag is orphaned: notify user
        if await sendorphan(params[2], message, client):
            return

        update = False

        tags[params[2]]['owner'] = member.id

        if tags[params[2]]['server'] != message.server.id:
            tags[params[2]]['server'] = message.server.id
            update = True

        updatetags()
        if update:
            await client.send_message(message.channel, '❤ {}: You have successfully given the tag {} to {}. I have also taken the liberty to update the tag\'s server location to this server.'.format(
                message.author.display_name,
                params[2],
                member.name
                ))
        else:
            await client.send_message(message.channel, '❤ {}: You have successfully given the tag {} to {}.'.format(
                message.author.display_name,
                params[2],
                member.name
                ))
        return
    #end gift

    if params[1] == 'claim':
        if not await totalparams('gift', 3, len(params), message, client):
            return

        if params[2] not in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: I could not find a tag with that name.\n*(In order to prevent orphaned tags with invalid names from being stuck, you must type the exact name of the tag. Substitution does not occur for this command.)*'.format(
                    message.author.display_name
                    )
                )
            return

        if tags[params[2]]['owner'] != 'None':
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: That tag is not orphaned.'.format(
                    message.author.display_name
                    )
                )
            return

        tags[params[2]]['owner'] = member.id
        tags[params[2]]['server'] = message.server.id

        updatetags()
        await client.send_message(message.channel, '🚸 {}: You now own the tag {}.'.format(
            message.author.display_name,
            params[2]
            ))
    #end claim

    if params[1] == 'orphan':
        if not await totalparams('gift', 3, len(params), message, client):
            return

        params[2] == await sub(params[2], message, client)

        if params[2] not in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: I could not find a tag with that name.'.format(
                    message.author.display_name
                    )
                )
            return

        if tags[params[2]]['owner'] != message.member.id:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: You do not have permission to modify this tag.'.format(
                    message.author.display_name
                    )
                )
            return


        tags[params[2]]['owner'] = 'None'
        tags[params[2]]['server'] = 'None'

        await client.send_message(
            message.channel,
            '{} {}: You have orphaned the tag `{}`.'.format(
                random.choice(
                    [
                        '\U0001F466', # :boy:
                        '\U0001F467'  # :girl:
                    ]
                    ),
                message.author.display_name,
                params[2]
                )
            )

    #end orphan

    if params[1] == 'recall':
        if not message.channel.is_private:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: This option can only be used in direct messages.'.format(
                    message.author.display_name
                    )
                )
            return

        if not await totalparams('recall', 3, len(params), message, client):
            return

        if params[2] not in tags:
            await client.send_message(
                message.channel,
                '\U0001F6AB {}: The tag `{}` does not exist.'.format(
                    message.author.display_name,
                    params[2]
                    )
                )
            return

        reasons = []

        # tag name contains capitals
        if params[2] != params[2].lower():
            reasons.append('Message name contains capitalized characters. Remedy: `rename` the tag to itself (if available) and the name will be automatically corrected. (`rename` is case insensitive for the first parameter.)')

        # tag name contains restricted characters, not including capitals
        if params[2] != limit.sub('', params[2].lower()) and limit.sub('', params[2].lower()) != params[2].lower():
            reasons.append('Message name contains nonalphanumeric characters, not including dashes or underscores. Remedy: `rename` the tag, removing the invalid characters. (`rename` is case insensitive for the first parameter.)')

        # tag name is reserved
        if params[2] in reserved:
            reasons.append('Tag name is reserved. Remedy: `rename` the tag to a new one. (`rename` is case insensitive for the first parameter.)')

        # tag contains mentions
        if not valid(tags[params[2]]['tag']):
            reasons.append('Includes a user mention, "@\u2060everyone", or "@\u2020here". Remedy: `edit` the tag, removing the offending lines. (This tag may need to be `rename`d first.)')

        await client.send_message(
            message.channel,
            '\u2139 {}: This is the tag `{}`.\n{}'.format(
                message.author.display_name,
                params[2],
                tags[params[2]]['tag']
                )
            )

        await client.send_message(
            message.channel,
            'This tag was disabled for the following reasons:\n*{}*\nResolve these problems, and you will be allowed to use the tag in standard channels again.'.format(
                '*\n*'.join(reasons)
                )
            )

        return
    # end recall

    params[1] = await sub(params[1], message, client)

    if params[1] not in tags:
        await client.send_message(
            message.channel,
            '\U0001F6AB {}: I could not find a tag with that name.\n*(Implicit creation is currently unavailable. Please use `create`.)*'.format(
                message.author.display_name
                )
            )
        return

    if not valid(tags[params[1]]['tag']):
        await client.send_message(
            message.channel,
            '\U0001F6AB {}: This tag currently features invalidations that must be remedied. Please use `{}tag recall <tag name>` in a direct message with me.'.format(
                message.author.display_name,
                base.config['invoker']
                )
            )
        return

    await client.send_message(
        message.channel,
        '\u2060' + tags[params[1]]['tag']
        )
    return
