import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ['Undertale', 'Big `.determinate` update!'],
    ['Undertale', 'We now use Inkscape for clearer quality and better portability.'],
    ['Undertale', 'The message will fall back to white if an invalid color is specified.'],
    ['Undertale', '`font=sans` is now forced lowercase. `font=papyrus` is forced uppercase.'],
    ['Undertale', 'RAINBOW easter egg now prints the color used.'],
    ['Undertale', 'The docstring was fixed.'],
    ['Undertale', 'You can now type `colour` instead of `color`!'],
    ['Undertale', 'More syntax! Use `color=`, `color:`, `colour=`, or even `colour:`! `font:` works too.'],
    ['all', 'Added syntax for printing tag amounts from the bot `42`.'],
    ['all', '`.quote` doesn\'t send an error message after sending a random quote anymore.'],
    ['all', 'Some funny, inconsequential stuff for `.quote`.']
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
