import cacobot.base as base
import time, re, urllib.request, html

@base.cacofunc
def roll(message, client, *args, **kwargs):
    '''
    **.roll**
    *This command was created for the /g/ server.*
    Generates an integer based on the current time. If the last two digits are equivalent, appends the message with 'check 'em!'
    *Example: `.roll`*
    '''

    # This was written by @NoKeksGiven. Give that guy a shout-out!
    num = str(round(int(round(time.time() * 100) % 100000000)))
    if num[-1] == num[-2]:
        yield from client.send_message(message.channel, '{}: {}, check \'em!'.format(message.author.mention, num))
    else:
        yield from client.send_message(message.channel, '{}: {}'.format(message.author.mention, num))
roll.server = '/g/'

@base.postcommand
def parseFor4chThread(message, client, *args, **kwargs):
    '''
    Parses for a 4chan thread in the message, and sends the linked message.
    '''

    # parse string as regex, capture the following:
    # 1. Whole URL
    # 2. thread ID
    # 3. either string "#p" or nothing (practically unused)
    # 4. linked post ID
    p = re.search('(https{0,1}://boards\.4chan\.org/.*/thread/([0-9]*)(#p){0,1}([0-9]*))', message.content)

    # continue if 4chan thread found
    if p:

        # download thread html as string
        thread = urllib.request.urlopen(p.group(1)).read().decode('UTF-8')

        # no image by default
        fname = None

        # get thread subject via title tag
        threadtitle = re.search('<title>/.*/ - (.*) - .* - 4chan</title>', thread).group(1)

        # if group 3 doesn't have "#p", then no post was linked. Just grab OP.
        if p.group(3):
            pindex = thread.find('id="p{}"'.format(p.group(4)))
            pmsg = thread.find('id="m{}"'.format(p.group(4)), pindex)
            pfile = thread.find('id="f{}"'.format(p.group(4)), pindex)
        else:
            pindex = thread.find('id="p{}"'.format(p.group(2)))
            pmsg = thread.find('id="m{}"'.format(p.group(2)), pindex)
            pfile = thread.find('id="f{}"'.format(p.group(2)), pindex)

        # if post had a file attached, fetch it.
        if pfile != -1:
            fname = 'https:' + re.search('href="(//i\.4cdn\.org/[^"]*/[^"]*)"', thread[pfile:]).group(1)

        # extract post message: replace line breaks and remove/unescape HTML.
        msg = re.search('id="m[0-9]*">(.*?)</blockquote>', thread[pmsg:]).group(1)
        msg = msg.replace('<br>', '\n')
        msg = html.unescape(re.sub('<[^<]+?>', '', msg))

        # do not continue if more than 6 line breaks exist
        if len(re.findall('\n', msg)) <= 6:

            # determine if post or thread again: add relevant text.
            if p.group(3):
                msg = '__**Linked post from 4chan thread "{}":**__\n{}'.format(threadtitle, msg)
            else:
                msg = '__**Linked thread from 4chan: "{}":**__\n{}'.format(threadtitle, msg)

            # if file: append it
            if fname:
                msg += '\n\n{}'.format(fname)

            # send
            yield from client.send_message(message.channel, msg)
    return
