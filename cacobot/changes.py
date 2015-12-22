import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ["all", "If you can manage roles in a server, you are allowed to delete tags. This is on trial: Abuse will lead to this function being removed."],
    ['all', 'Call `.git` to quickly be linked to the CacoBot Repo on Github. Call `.git [*file*]` to get a link to a specific file. (I.E. `.git cacobot/base.py`)'],
    ['all', 'Changed the `.connect` example to link to CacoServer'],
    ['all', 'CacoBot stopped playing games for some reason. That should be fixed.'],
    ["Undertale", "Increased the size of the Papyrus font in .determinate... but tentatively."],
    ["Undertale", "`.summon` should stop throwing errors on the special cases."],
    ["Undertale", "Decreased WD font size and line height."],
    ["Undertale", "Added a shortcut to `.determinate` through `.say!`"],
    ["Undertale", "Fixed a glitch where `.summon` only posted the spoiler-free list in all channels."],
    ["Undertale", "Fixed a glitch where `.summon` with no valid monster codes resulted in summoning Jerry."]
]

# There's a few more emojis I could use for bullets, but these stuck out the most to me.
emojis = [":black_small_square:", ":small_blue_diamond:", ":small_orange_diamond:", ":small_red_triangle:"]

@base.cacofunc
def changes(message, client, *args, **kwargs):
    """
    **.changes**
    Displays the most recent CacoBot changes.
    *Example: .changes*
    """

    printChanges = "{}: **Latest Changes**\n".format(message.author.mention())

    for x in change_list:
        if message.channel.is_private:
            if x[0] == 'all':
                printChanges += "{} {} \n".format(random.choice(emojis), x[1])
        else:
            if x[0] == 'all' or message.server.name == x[0]:
                printChanges += "{} {} \n".format(random.choice(emojis), x[1])

    yield from client.send_message(message.channel, printChanges)
