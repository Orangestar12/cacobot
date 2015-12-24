import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ['all', '`.quote` no longer exposes an error when the index is out of range.'],
    ['all', '`.addquote` no longer allows you to add duplicates.'],
    ['all', '`.myid` can give you your ID, in case another bot with a more verbose info command is offline.'],
    ['all', 'CacoBot plays more 90s shooters, thanks to the death of `game_id`!'],
    ['all', '`.choice` is now based on semicolons, not commas. I.E. `.choice One; Two`'],
    ['all', 'Docstrings should now display commands in `code blocks.` Try it out by calling `.help` with your favorite command.'],
    ['all', '`.yt` Now only returns *one video* unless you set `.results`. No more searching playlists or channels with it: It was unused.'],
    ['Undertale', 'More monsters for `.summon`, thanks to ToransuShojo!']
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
