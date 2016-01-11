import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ['all', '**CacoBot now has a Terms of Service.** You should check it out here: https://github.com/Orangestar12/cacobot/blob/master/tos.md'],
    ['all', 'CacoBot is now versioned! I don\'t know how many revisions we\'ve had so let\'s just say we\'re on r20 now.'],
    ['all', '`.connect` and `.choice` now print properly-formatted error messages on incorrect input.'],
    ['all', 'Memos are no longer sent to you if you\'re mentioned in a channel you cannot read.'],
    ['all', '`.delquote` now prints the correct deleted quote index.'],
    ['all', 'Check out `.welcome` if you\'re completely in the dark about CacoBot!'],
    ['all', 'I\'ve done a little more catagorization of commands for `.help`.'],
    ['Vocaloid/UTAU', 'Administrators can now call `.limbo` to quickly roleban users, or to roleban on mobile.'],
    ['all', '**Changes since r19 below:**'],
    ['all', '`.log` now sends in <2000 character bursts.'],
    ['all', 'Tag listing is now done through Pastebin.'],
    ['all', '`.delquote` and `.parsequote` are live!'],
    ['all', '`.stats` uses Inkscape too, now.'],
    ['Undertale', '`.determinate`: `color=rainbow` is now a feature.'],
    ['Undertale', '`.determinate`: We now use Inkscape for printing.'],
    ['Undertale', '`.forebode`\'s docstring had typos. That was fixed.']
]

# There's a few more emojis I could use for bullets, but these stuck out the most to me.
emojis = [':black_small_square:', ':small_blue_diamond:', ':small_orange_diamond:', ':small_red_triangle:']

@base.cacofunc
def changes(message, client, *args, **kwargs):
    '''
    **.changes**
    Displays the most recent CacoBot changes.
    *Example: `.changes`*
    '''

    printChanges = '{}: **Latest Changes**\n'.format(message.author.mention)

    for x in change_list:
        if message.channel.is_private:
            if x[0] == 'all':
                printChanges += '{} {} \n'.format(random.choice(emojis), x[1])
        else:
            if x[0] == 'all' or message.server.name == x[0]:
                printChanges += '{} {} \n'.format(random.choice(emojis), x[1])

    yield from client.send_message(message.channel, printChanges)
