import cacobot.base as base
import random # To print random emojis.

# This list is at the top so you can easily change it. The first parameter of
# the list is a server name: Use 'all' to send to all servers, or type a server
# name to make that server the only one that can see that change.
change_list = [
    ["all", "I fixed that glitch where you can't use tags in DMs."],
    ["all", "We Github now. https://github.com/Orangestar12/cacobot"],
    ["all", "Call .tag list mine and paste the result back into the channel: CacoBot will count your tags!"],
    ["all", ".tag list now lists only the tags created in the server you've posted the command now. Use .tag list all to list all tags."],
    ["all", "New! .choice!"],
    ["all", "YouTube search is back! Use .yt."],
    ["all", "Cacobot should now get a random game ID once every so often!... In theory."],
    ["all", "Hotfix: Fixed a glitch where you couldn't claim tags in DMs."],
    ["all", "Hotfix: Fixed a glitch where log would send over 3000 seconds instead of 3."],
    ["all", "Hotfix: Fixed the timing on CacoBot so he changes games every hour instead of every 16 hours."],
    ["/g/entoo", "STILL COMING SOON: Radio?"],
    ["Undertale", ".summon is now back and better than ever! You can present as many monster codes as you want, space-seperated, and case doesn't matter anymore!"],
    ["Undertale", ".determinate now has a new function where you can provide a space-seperated specific font. I don't have a lot of fonts, so maybe suggest a few? Example: font=Segoe_UI_Semilight"],
    ["Undertale", "Something else? `:^)`"],
    ["Undertale", "Hotfix: Fixed a glitch where summon still required correct casing."],
    ["Undertale", "Hotfix: Fixed a glitch where summon threw an error with an empty array of characters."],
    ["Undertale", "Hotfix: Installed those extra fonts."],
    ["Undertale", "Hotfix: Fixed an exploit where making every single summon \"Jerry\" caused an array of indecipherable gibberish to spawn instead."],
    ["Undertale", "Hotfix: Fixed a typo that caused special summon cases not to occur."]
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
