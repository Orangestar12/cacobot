import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ["all", "SOON: I'm gonna fix that glitch where you can't use tags in DMs."],
    ["all", "We Github now. https://github.com/Orangestar12/cacobot"],
    ["all", "Call .tag list mine and paste the result back into the channel: CacoBot will count your tags!"],
    ["all", ".tag list now lists only the tags created in the server you've posted the command now. Use .tag list all to list all tags."],
    ["all", "New! .choice!"],
    ["all", "YouTube search is back! Use .yt."],
    ["/g/entoo", "STILL COMING SOON: Radio?"],
    ["Undertale", ".summon is now back and better than ever! You can present as many monster codes as you want, space-seperated, and case doesn't matter anymore!"],
    ["Undertale", ".determinate now has a new function where you can provide a space-seperated specific font. I don't have a lot of fonts, so maybe suggest a few? Example: font=Segoe_UI_Semilight"],
    ["Undertale", "Something else? `:^)`"]
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
