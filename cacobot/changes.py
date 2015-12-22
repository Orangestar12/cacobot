import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ['all', 'I fixed `.stats`. Sorry.'],
    ['all', 'Now @*everyone* mentions *actually do* memo you if you\'re on the memo list.'],
    ['all', 'Memos were made less API-intensive. I made the guarantee that the message would send a higher priority than sending the message quickly. You will definitely recieve memos (And now all as 1 message!)'],
    ['all', '`.stats` is now nondescriminatory. To be fair it was already, but now we shuffle the list so the order is not based on Python quirks anymore.'],
    ["Undertale", "Special cases in `.summon` are finally definitely, *unconditionally* unbroken."],
    ['Undertale', '`.summon` now removes duplicates.'],
    ['Undertale', 'Unbroke `.say`. Sorry...']
]

# There's a few more emojis I could use for bullets, but these stuck out the most to me.
emojis = [':black_small_square:', ':small_blue_diamond:', ':small_orange_diamond:', ':small_red_triangle:']

@base.cacofunc
def changes(message, client, *args, **kwargs):
    '''
    **.changes**
    Displays the most recent CacoBot changes.
    *Example: .changes*
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
