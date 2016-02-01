import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ['all', 'You may now opt out of recieving memos on everyone mentions by doing `.memo mentions`.'],
    ['all', 'Limitations have been added to `.d` to ease up on Cacobot\'s memory usage.'],
    ['all', '`.tag list all` has been fixed, and will now auto-orphan tags if Caco isn\'t in a server anymore.'],
    ['all', '`.journal` has been fixed.'],
    ['all', '4chan posting is slightly better now: Posts truncate to 6 newlines and support all links. Get an untruncated post by preceding the link with `+`. Disable this functionality by preceding the link with `.`'],
    ['all', '**__Changes since revision 22.__**'],
    ['all', 'Less errors with `.tag` and `.determinate`.'],
    ['all', '`.log` now sends markdown unparsed! This means that "Uncle Phil you got to kick that man\'s __***BUTT***__" will come out as "Uncle Phil you got to kick that man\'s \_\_\*\*\*BUTT\*\*\*\_\_"'],
    ['Dream Journals', 'Introducing the `.journal` command! Creates a public channel that only you can post in!'],
    ['Vocaloid/UTAU', 'Fixed a typo where `.limbo` was referred to as `.forebode` in its docstring.'],
    ['Undertale', 'Check out `.ship`. ( ͡° ͜ʖ ͡°)'],
    ['all', 'Tag listing has become confusing and verbose for most bots. Hence, automatic tag listing has been removed. Sorry if you still used it.'],
    ['Undertale', '`.What was his name again?` You know, the firey guy from Hotland?'],
    ['all', 'CacoBot now posts 4chan posts that you link! (This doesn\'t work with semantic URLs, yet.)'],
    ['all', 'In case you haven\'t noticed, CacoBot can shitpost, now. It\'s a 1/9001 chance to happen.'],
    ['all', '`.quote` *should* strip out mentions now!'],
    ['all', 'Generate fortune cookies with `.fortune`!'],
    ['all', 'Snuck in `.later`. ( ͡° ͜ʖ ͡°)']
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
