import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ['all', '**This bot is running CacoBot, Revision 21!**'],
    ['all', '`.urbdef` and `.define` now give proper error messages instead of general ones when you provide nothing to search for.'],
    ['all', '`.tag list`ing goes through Pastebin now. **LIST ALL THE TAGS!**'],
    ['all', '`.determinate` no longer forcibly uppercases or lowercases your words, unless you use Wingdings, because I got a lot of flack for that.'],
    ['all', 'You should now be able to put `font=XXX` and `color=XXX` at the *END* of your `.determinate` messages!'],
    ['all', 'Moderators: Include `.nuke` and `.cleanup` into your repertoire. `.nuke` deletes a numeric amount of messages, while `.cleanup` removes just bot commands! **These commands are extremely dangerous. Consider reforming your moderation team if they are spammed.**'],
    ['all', 'Fixed some typos in `.welcome`.'],
    ['all', 'I think I finally, *actually* fixed `.delquote` this time. Ugh.']
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
