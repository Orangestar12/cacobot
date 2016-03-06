import html
import re
import random
import time
import urllib.request

import cacobot.base as base

@base.cacofunc
async def roll(message, client):
    '''
    **.roll**
    *This command was created for the /g/ server.*
    Generates an integer based on the current time. If the last two digits are equivalent, appends the message with 'check 'em!'
    *Example: `.roll`*
    '''

    # This was written by @NoKeksGiven. Give that guy a shout-out!
    num = str(round(int(round(time.time() * 100) % 100000000)))
    if num[-1] == num[-2]:
        await client.send_message(message.channel, '{}: {}, check \'em!'.format(message.author.mention, num))
    else:
        await client.send_message(message.channel, '{}: {}'.format(message.author.mention, num))
roll.server = '/g/'

@base.postcommand
async def parseFor4chThread(message, client):
    '''
    Parses for a 4chan thread in the message, and sends the linked message.
    '''

    # parse string as regex, capture the following:
    # 1. Whole URL
    # 2. thread ID
    # 3. The semantic thread URL, if available (unused)
    # 4. either string "#p and post ID" or nothing (practically unused)
    # 5. linked post ID
    restring = r'(https?:\/\/boards\.4chan\.org\/.*?\/thread\/([0-9]*)(\/[a-z0-9-]*)?\/?(#p([0-9]*))?)'

    p = re.search(restring, message.content)
    q = re.search(r'\.' + restring, message.content)

    # continue if 4chan thread found
    if p and not q:
        # download thread html as string
        thread = urllib.request.urlopen(p.group(1)).read().decode('UTF-8')

        # no image by default
        fname = None

        # get thread subject via title tag
        threadtitle = re.search('<title>/.*/ - (.*) - .* - 4chan</title>', thread).group(1)

        # if group 5 doesnt exist, then no post was linked. Just grab OP.
        if p.group(5):
            pindex = thread.find('id="p{}"'.format(p.group(5)))
            pmsg = thread.find('id="m{}"'.format(p.group(5)), pindex)
            pfile = thread.find('id="f{}"'.format(p.group(5)), pindex)
        else:
            pindex = thread.find('id="p{}"'.format(p.group(2)))
            pmsg = thread.find('id="m{}"'.format(p.group(2)), pindex)
            pfile = thread.find('id="f{}"'.format(p.group(2)), pindex)

        # if post had a file attached, fetch it.
        if pfile != -1:
            fname = 'https:' + re.search(r'href="(//i\.4cdn\.org/[^"]*/[^"]*)"', thread[pfile:]).group(1)

        # extract post message: replace line breaks and remove/unescape HTML.
        msg = re.search(r'id="m[0-9]*">(.*?)</blockquote>', thread[pmsg:]).group(1)
        msg = msg.replace('<br>', '\n')
        msg = html.unescape(re.sub(r'<[^<]+?>', '', msg))

        # determine if post or thread again: add relevant text.
        if p.group(3):
            msg = '__**Linked post from 4chan thread "{}":**__\n{}'.format(threadtitle, msg)
        else:
            msg = '__**Linked thread from 4chan: "{}":**__\n{}'.format(threadtitle, msg)

        # do not post more than 6 lines unless preceded with "+"
        if not re.search(r'\+' + restring, message.content):
            if len(msg.split('\n')) > 7:
                msg = '\n'.join(msg.split('\n')[:7]) + '...'

        # if file: append it
        if fname:
            msg += '\n\n{}'.format(fname)

        # send
        await client.send_message(message.channel, msg)
    return

@base.postcommand
async def cake(message, client):
    if not message.channel.is_private and message.server.id == '120205773425868804':
        c = re.sub(r'[^A-Za-z0-9 ]', '', message.content.lower())
        send = None
        if message.author.id != client.user.id:
            if c == 'kek':
                send = 'Cake*'

        if send:
            if random.randint(1, 2) == 1:
                await client.send_message(message.channel, send)
