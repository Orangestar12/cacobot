import random
import subprocess

import discord

import cacobot.base as base

# No comments. Fuck you.

@base.cacofunc
async def goatnick(message, client):
    '''
    **{0}goatnick**
    *This command was created for the Undertale server.*
    Generates a politically incorrect name for Asgore from a list.
    *Example: `{0}goatnick`*
    '''
    asgore_nicks = [
        'King Kindergarten Killer',
        'Spike The Tyke',
        'Ankle-Biter Beater',
        'Crying Child Crusher',
        'Non-Senior Citizen Slayer',
        'Toddler Terminator',
        'Munchkin Murderer',
        'Innocent Infanticider',
        'Punt The Runt',
        'Mourning Mother-Maker',
        'Child Coffin Collector',
        'Youngster Euthanizer',
        'Splat The Brat',
        'Be Mean To Teens',
        'Maybe Killed A Baby',
        'Gerber Grow-Up Plan Gleaner',
        'Preschool Purifier',
        'When They Hit The Flowers, They’re Dead In Hours',
        'Extra-Small Exterminator',
        'Kiddy Cleanser',
        'You Must Be This Tall To Live',
        'Crueler for the Preschooler',
        'Offspring Annihilator',
        'Get Rid Of The Kid',
        'Infant Slayer Player',
        'Stabbed Some Kids Through The Ribs',
        'Trust Fund Refund',
        'Playground Flaying Round',
        'Adolescent Suppressant',
        'Youthanizer',
        'Out Of The Womb, Into The Tomb',
        'No Longer Married Cause Some Kids Got Buried',
        'My Hobbies Include Child Murder',
        'Big Sad Goat Dad',
        'T&T TNT',
        'A child a day keeps the wife away',
        'If it\'s under eleven, I\'ll send them to heaven',
        'The Undertale Underage Undertaker',
        'The Kindergarten Harvester',
        'The Daycare Decimator',
        'Nipper Annihilator',
        'Moppet Mopper-Upper',
        'I\'ll Fix Yah With Asphyxia',
        'Best Child Murderer \'9X',
        'Alone in bed \'cause some kids are dead',
        'Adam Lanza\'s number one Fan-za',
        'The chiller child killer',
        'Half-pint Holocaust',
        'Fell into my cave, right into the grave',
        'Better at Infanticide than Isaac\'s mom',
        'Where Flowey gets his kill skill from',
        'Bury the youngster six feet under',
        'Dunks the little punks',
        'No MERCY for Li\'l Percy',
        'My kids an hero\'ed so I went 6/0',
        'I don\'t have a car in my garage'
    ]
    await client.send_message(message.channel, '{}: Asgore "{}" Dreemurr'.format(message.author.mention, random.choice(asgore_nicks)))
goatnick.server = 'Undertale'

@base.cacofunc
async def summon(message, client):
    '''
    **{0}summon** [*monster 1*] [*monster 2*]...
    *This command was created for the Undertale server.*
    Prints the array of [*monster*]s's encounter texts. Provide as many encounters as you want, or leave it blank to summon a random one.
    *Example: {0}summon Papyrus Snowdrake*
    '''
    monsters = {
        'Dummy' : 'You encountered the dummy.',
        'Froggit' : 'Froggit hopped close!',
        'Whimsun' : 'Whimsun appeared meekly.',
        'Moldsmal' : 'You tripped into a line of Moldsmals.',
        'Loox' : 'Loox drew near!',
        'Napstablook' : 'Here comes Napstablook.',
        'Vegetoid' : 'Vegetoid came out of the earth!',
        'Migosp' : 'Migosp crawled up close!',
        'Toriel' : 'Toriel blocks the way!',
        'Snowdrake' : 'Snowdrake flutters forth!',
        'IceCap' : 'Icecap struts into view.',
        'Gyftrot' : 'Gyftrot confronts you!',
        'Doggo' : 'Doggo is too suspicious of your movements.',
        'Dogi' : 'Dogi assault you!',
        'LesserDog' : 'Lesser Dog appears.',
        'GreaterDog' : 'It\'s the Greater Dog.',
        'Papyrus' : 'Papyrus blocks the way!',
        'Aaron' : 'Aaron flexes in!',
        'Moldbygg' : 'You tripped into a line of Moldsmals.',
        'Woshua' : 'Woshua shuffles up.',
        'Temmie' : 'Special enemy Temmie appears here to defeat you!!',
        'MadDummy' : 'Mad Dummy blocks the way!',
        'Shyren' : 'Shyren hides in the corner but somehow encounters you anyway.',
        'Undyne' : 'Undyne attacks!',
        'Vulkin' : 'Vulkin strolls in.',
        'Tsunderplane' : 'Tsunderplane gets in the way! Not on purpose or anything.',
        'Pyrope' : 'Pyrope bounds towards you!',
        'RG' : 'Royal Guard attacks!',
        'Muffet' : 'Muffet traps you!',
        'FinalFroggit' : 'Final Froggit was already there, waiting for you.',
        'Whimsalot' : 'Whimsalot rushed in!',
        'Astigmatism' : 'Eyes appeared from the shadows.',
        'Madjick' : 'Madjick pops out of its hat!',
        'KnightKnight' : 'Knight Knight blocks the way!',
        'Mettaton' : 'Mettaton attacks!',
        'MettatonEX' : 'Mettaton EX makes his premiere!',
        'Asgore' : 'ASGORE attacks!'
    }
    spoilers = {
        'Childrake' : 'Childrake saunters up!',
        'Undying' : 'The heroine appears.',
        'GladDummy' : 'Glad Dummy lets you go.',
        'MettatonNEO' : 'Mettaton NEO blocks the way!',
        'Sans' : 'You feel like you\'re gonna have a bad time.',
        'Asriel' : 'It\'s the end.',
        'LemonBread' : 'Smells like sweet lemons.',
        'ReaperBird' : ',',
        'Amalgamate' : 'It\'s so cold.',
        'Memoryhead' : 'drew near!',
        'Endogeny' : 'It\'s the Amalgamate.',
        'MonsterKid' : 'In my way.',
        'LostSoul' : 'The Lost Soul appeared.',
        'LostSouls' : 'The Lost Souls appeared.',
        'TestFroggit' : 'TestMonster and its cohorts drew near!'
    }
    hidden = {
        'Glyde' : 'Glyde swooped in!',
        'SoSorry' : 'You\'re blocked in politely!'
    }

    # Just summon
    if message.content.strip()[len(base.config['invoker']):] == 'summon':
        monsters.update(spoilers)

        # 1 in 50 chance to add hidden monsters to rotation
        if random.randrange(1, 50) == 1:
            monsters.update(hidden)

        msg = '```\n' + monsters[random.choice(list(monsters))]

        # 1 in 1k chance to spawn Jerry
        if random.randrange(0, 20) == 1:
            msg += '\nJerry came, too.'

        msg += '\n```'

        await client.send_message(message.channel, msg)

    elif message.content.strip()[len(base.config['invoker']):] == 'summon list':
        monsters.update(spoilers)
        monsters.update(hidden)

        await client.send_message(message.channel, 'List of Monster Codes:\n```\n{}\n```'.format(' '.join(sorted(list(monsters)))))

    else:
        cmd = message.content.split()[len(base.config['invoker']):]
        msg = []

        monsters.update(hidden)

        for x in cmd:
            for y in monsters:
                if x.lower() == y.lower():
                    msg.append(monsters[y])
                    break
                if x.lower() == 'jerry':
                    msg.append('Jerry came, too.')

        # Detect special cases

        # KK & Madjick: Mercenaries
        if issublist(['Madjick pops out of its hat!', 'Knight Knight blocks the way!'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Knight Knight blocks the way!'][0]
            msg.remove('Madjick pops out of its hat!')
            msg.remove('Knight Knight blocks the way!')
            msg.insert(save, 'Mercenaries emerge from the shadows.')

        # Pyrope & Pyrope: Double Davis
        if issublist(['Pyrope bounds towards you!', 'Pyrope bounds towards you!'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Pyrope bounds towards you!'][0]
            msg.remove('Pyrope bounds towards you!')
            msg.remove('Pyrope bounds towards you!')
            msg.insert(save, 'The rare and threatening Double Davis.')

        # Vulkin + Tsun: Jealous
        if issublist(['Tsunderplane gets in the way! Not on purpose or anything.', 'Vulkin strolls in.'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Tsunderplane gets in the way! Not on purpose or anything.'][0]
            msg.remove('Tsunderplane gets in the way! Not on purpose or anything.')
            msg.remove('Vulkin strolls in.')
            msg.insert(save, 'Tsunderplane attacks! Not because it\'s jealous Vulkin is paying attention to you.')

        # Vulkin + Vulkin: Strange Parade
        if issublist(['Vulkin strolls in.', 'Vulkin strolls in.'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Vulkin strolls in.'][0]
            msg.remove('Vulkin strolls in.')
            msg.remove('Vulkin strolls in.')
            msg.insert(save, 'A strange parade blocks the path.')

        # Aaron + Woshua: Easter Egg
        if issublist(['Aaron flexes in!', 'Woshua shuffles up.'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Aaron flexes in!'][0]
            msg.remove('Aaron flexes in!')
            msg.remove('Woshua shuffles up.')
            msg.insert(save, 'Woshua and Aaron appear.')

        # Snowdrake + Ice Cap: pose
        if issublist(['Snowdrake flutters forth!', 'Ice Cap struts into view.'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Snowdrake flutters forth!'][0]
            msg.remove('Snowdrake flutters forth!')
            msg.remove('Icecap struts into view.')
            msg.insert(save, 'Icecap and Snowdrake pose like bad guys.')

        # Loox + Veg/Migosp: loox & Co.
        if issublist(['Loox drew near!', 'Vegetoid came out of the earth!', 'Migosp crawled up close!'], msg) or issublist(['Loox drew near!', 'Vegetoid came out of the earth!'], msg) or issublist(['Loox drew near!', 'Migosp crawled up close!'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Loox drew near!'][0]
            msg.remove('Loox drew near!')
            try:
                msg.remove('Migosp crawled up close!')
            except (IndexError, ValueError):
                pass
            try:
                msg.remove('Vegetoid came out of the earth!')
            except (IndexError, ValueError):
                pass
            msg.insert(save, 'Loox and co. decided to pick on you!')

        # Two Moldsmal: Moldsmal and Moldsmal
        if issublist(['You tripped into a line of Moldmals.', 'You tripped into a line of Moldmals.'], msg):
            save = [i for i, x in enumerate(msg) if x == 'You tripped into a line of Moldmals.'][0]
            msg.remove('You tripped into a line of Moldmals.')
            msg.remove('You tripped into a line of Moldmals.')
            msg.insert(save, 'Moldsmal and Moldsmal block the way.')

        # Astig, FF, Whim: ULTRA-VIOLENCE
        if issublist(['Whimsalot rushed in!', 'Final Froggit was already there, waiting for you.', 'Eyes appeared from the shadows.'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Final Froggit was already there, waiting for you.'][0]
            msg.remove('Eyes appeared from the shadows.')
            msg.remove('Whimsalot rushed in!')
            msg.remove('Final Froggit was already there, waiting for you.')
            msg.insert(save, 'What a nightmare!')

        # Astig + FF: Not correct...
        if issublist(['Final Froggit was already there, waiting for you.', 'Eyes appeared from the shadows.'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Final Froggit was already there, waiting for you.'][0]
            msg.remove('Eyes appeared from the shadows.')
            msg.remove('Final Froggit was already there, waiting for you.')
            msg.insert(save, 'That doesn’t seem correct.')

        # Whimsalot + FF: Believe it?
        if issublist(['Final Froggit was already there, waiting for you.', 'Whimsalot rushed in!'], msg):
            save = [i for i, x in enumerate(msg) if x == 'Final Froggit was already there, waiting for you.'][0]
            msg.remove('Whimsalot rushed in!')
            msg.remove('Final Froggit was already there, waiting for you.')
            msg.insert(save, 'Can you believe it?')

        # Duplicate removal
        # from http://www.dotnetperls.com/remove-duplicates-list-python
        output = []
        for value in msg:
            if value not in output:
                output.append(value)
        msg = output

        # if 'Jerry came, too.' in msg and len(msg) == len([x for x in msg if x == 'Jerry came, too.']):
        #     msg = ['Jerry came, too.']

        # detect jerry
        while msg and msg[0] == 'Jerry came, too.':
            if len(msg) == 1:
                msg.insert(0, monsters[random.choice(list(monsters))])
            else:
                msg.append(msg.pop(0))

        if msg:
            await client.send_message(message.channel, '```\n{}\n```'.format('\n'.join(msg)))
        else:
            await client.send_message(message.channel, '{}: I could not find any valid monster codes in your query. Use .summon list to see them all.'.format(message.author.mention))
summon.server = 'Undertale'

@base.cacofunc
async def determinate(message, client):
    r'''
    **{0}determinate** [color\=*color*] [font\=*font*] <*text*>
    *This command was created for the Undertale server.*
    Generates an image with text of your choice using the font Determination Mono. [color\=*color*] can be provided as a CSS color, like hexadecimal (#FF7700), rgb (rgb(255,128,0)), or color code (orange). [font=*font*] can be *sans*, *papyrus*, *wd*, or *ut*. Omit to leave it as DTM.
    You can also use colons instead of equals signs. If you specify a font not in our keys using underscores in place of spaces, you can specify other fonts, like `font=Roboto_Condensed`.
    *Example: `{0}determinate color=#0000FF font=Papyrus YOU'RE BLUE NOW! THAT'S MY ATTACK.`*
    '''
    # The example used to be this:
    # *Example: .determinate color=#FF0000 Where are the knives.*
    # Then the spoiler rules got more strict so I had to change it.

    try:
        color = '#FFFFFF'
        font = 'Determination Mono'
        strokewidth = '0'
        lineheight = 36 #This is actually slightly big for the height of lines but *Shrug*
        fontwidth = 28
        precedent = 32
        width = '640'

        # I'm basically only using this to quickly strip ".determinate" from the message
        TextToSay = message.content.split(None, 1)[1]

        # find color
        if 'color=' in TextToSay.lower() or 'color:' in TextToSay.lower() or 'colour=' in TextToSay.lower() or 'colour:' in TextToSay.lower():
            if 'color=' in TextToSay.lower():
                findme = 'color='
            elif 'color:' in TextToSay.lower():
                findme = 'color:'
            elif 'colour=' in TextToSay.lower():
                findme = 'colour='
            elif 'colour:' in TextToSay.lower():
                findme = 'colour:'

            index = TextToSay.find(findme) + len(findme)
            end = TextToSay.find(' ', index)
            if end == -1:
                end = len(TextToSay)

            color = TextToSay[index:end]

            index = index - len(findme)

            end = end + 1
            if end > len(TextToSay):
                end = len(TextToSay)
            TextToSay = TextToSay[:index] + TextToSay[end:]

        rainbow = False
        if color.lower() == 'rainbow':
            clr = ['#']
            for x in range(0, 6):
                clr.append(random.choice('0123456789ABCDEF'))
            color = ''.join(clr)
            rainbow = True

        #find font
        if 'font=' in TextToSay.lower() or 'font:' in TextToSay.lower():
            if 'font=' in TextToSay.lower():
                findme = 'font='
            else:
                findme = 'font:'
            index = TextToSay.find(findme) + len(findme)
            end = TextToSay.find(' ', index)
            if end == -1:
                end = len(TextToSay)
            newfnt = TextToSay[index:end].lower()

            if newfnt == 'sans':
                font = 'Comic Sans MS'
                lineheight = 40
            elif newfnt == 'papyrus':
                font = 'Papyrus'
                strokewidth = '1'
                fontwidth = 20
            elif newfnt == 'wd':
                font = 'Wingdings'
                strokewidth = '1'
                fontwidth = 18
                lineheight = 24
            elif newfnt == 'ut':
                font = 'Monster Friend Fore'
                width = '700'
                precedent = 22
            else:
                font = newfnt.replace('_', ' ')

            index = index - 5
            end = end + 1

            if end > len(TextToSay):
                end = len(TextToSay)
            TextToSay = TextToSay[:index] + TextToSay[end:]

        TextToSay = TextToSay.strip()
        if font.lower() in ['wingdings', 'webdings']:
            TextToSay = TextToSay.upper()

        # true if "* " exists, false if it doesn't.
        indent = bool(TextToSay.startswith('* '))

        TextList = []

        while TextToSay:
            if indent:
                # Indent mode must determine whether the next string starts with
                # '* ' or not.
                # 'prec' is a variable I made to determine how many characters can
                # be on each line
                if TextToSay.startswith('* '):
                    prec = precedent
                else:
                    prec = precedent - 2
            else:
                prec = precedent

            fore = prec + 1

            if '\n' in TextToSay[:prec]:
                index = TextToSay.find('\n')
                TextList.append(TextToSay[:index])
                TextToSay = TextToSay[index+1:]

            else: # line break was not found
                try: # char 32 is a space
                    if TextToSay[prec] == ' ':
                        TextList.append(TextToSay[:prec])
                        TextToSay = TextToSay[fore:]
                    else:
                        # I could do this with a for loop, but the way I wanted it
                        # to be done worked much better with a While loop, so I used
                        # it instead.
                        x = prec-1
                        while True:
                            if x == -1:
                                TextList.append(TextToSay[:prec])
                                TextToSay = TextToSay[fore:]
                                break

                            elif TextToSay[x] in r' -\/':
                                # I include the line break so we can break things
                                # like "Democratic-Republican."" and keep the -.

                                # ...Sorry, that was a shitty example.

                                TextList.append(TextToSay[:x+1])
                                TextToSay = TextToSay[x+1:]
                                break

                            # After the loop, if we haven't broken, subtract x by 1
                            # so we can check the next character down in the next
                            # loop.
                            x = x-1

                # IndexError occurs when TextToSay is less than 32 characters
                # This means we can just shove the rest onto it wholesale
                except IndexError:
                    TextList.append(TextToSay)
                    TextToSay = '' # blank the var. This kills the loop.

        # end while TextToSay:

        if indent:
            #indent mode: indent messages
            for i, x in enumerate(TextList):
                if not x.startswith('* '):
                    TextList[i] = '  ' + x

        save = '\n'.join(TextList)
        for i, x in enumerate(TextList):
            TextList[i] = htmlEntities(x)
        lines = len(TextList)
        height = (lines * lineheight) + 94

        svgString = r'<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg width="' + width + '" height ="' + str(height) + '" viewBox="0 0 ' + width + ' ' + str(height) + '" xmlns="http://www.w3.org/2000/svg" version="1.1" shape-rendering="optimizeSpeed"><rect width="100%" height="100%" fill="black"/>'

        # MFF requires no rect and a back layer.
        if font != 'Monster Friend Fore':
            svgString += '<rect width="576" height="' + str(height - 64) + '" x="33" y="33" stroke-width="6" stroke="white"/>'
        else:
            y = 50
            svgString += '<text style="fill: white; fill:' + color + '; stroke: white; stroke:' + color + '" stroke-width="' + strokewidth + '" x="50" y="50" font-size="' + str(fontwidth) + 'px" font-family="Monster Friend Back" xml:space="preserve" opacity="0.65">'

            y = 50 + fontwidth
            for x in TextList:
                svgString += '<tspan x="50" y="' + str(y) + '">'+ x + '</tspan>'
                y += lineheight

            svgString += '</text>'

        svgString += '<text style="fill: white; fill:' + color + '; stroke: white; stroke:' + color + '" stroke-width="' + strokewidth + '" x="50" y="50" font-size="' + str(fontwidth) + 'px" font-family="' + font + '" xml:space="preserve">'

        y = 50 + fontwidth
        for x in TextList:
            svgString += '<tspan x="50" y="' + str(y) + '">'+ x + '</tspan>'
            y += lineheight

        svgString += '</text></svg>'

        # write svg
        with open('tmp.svg', 'w') as data:
            data.write(svgString)

        # requires inkscape
        subprocess.check_call(['inkscape', '-z', 'tmp.svg', '-e', 'tmp.png'])

        await client.send_file(message.channel, 'tmp.png')

        # Try to delete the message.
        try:
            await client.delete_message(message)
        except (discord.Forbidden, discord.HTTPException):
            # do nothing if no permission or message
            pass

        # send msg if wingdings
        if font.lower() in ['wingdings', 'webdings']:
            await client.send_message(message.channel, '*{}*'.format(save))

        # send author
        if rainbow:
            await client.send_message(message.channel, '*Color: {}*. \n*Sent by {}.*'.format(color, message.author.mention))
        else:
            await client.send_message(message.channel, '*Sent by {}.*'.format(message.author.mention))
    except IndexError:
        await client.send_message(
            message.channel,
            'If you do not know how to use this command, call `{0}help determinate`!'.format(
                base.config['invoker']
                )
            )
determinate.server = 'Undertale'

# You know, while I'm here, here's the StackOverflow post that has the function.
# It's really useful. Credit where it's due.
# http://stackoverflow.com/questions/18609778/solved-python3-convert-all-characters-to-html-entities
def htmlEntities(string):
    return ''.join(['&#{0};'.format(ord(char)) for char in string])

@base.cacofunc
async def forebode(message, client):
    '''
    **{0}forebode** [*mention*]
    This is a shortcut to add the "Foreboden" role to a user. If your server has no "Foreboden" role, this will fail.
    *Example: `{0}forebode @CacoBot`*
    '''
    if message.channel.permissions_for(message.author).ban_members:
        try:
            foreboden = discord.utils.find(lambda m: m.name == 'Foreboden', message.server.roles)
            if foreboden:
                for ment in message.mentions:
                    await client.replace_roles(ment, foreboden)
                    await client.send_message(message.channel, '{}: {} has been foreboden.'.format(message.author.mention, ment.name))
            else:
                await client.send_message(message.channel, '{}: You must create a role named \'Foreboden\' before you can use this command.'.format(message.author.mention))
        except discord.Forbidden:
            await client.send_message(message.channel, '{}: I do not have the permission to perform this command yet.'.format(message.author.mention))
    else:
        await client.send_message(message.channel, '{}: You do not have the permission to ban.'.format(message.author.mention))
forebode.server = 'Undertale'

@base.cacofunc
async def say(message, client):
    '''
    **{0}say** [*params*]
    A shorcut to `{0}determinate`.
    '''
    await determinate(message, client)

def issublist(sl, ml):
    sublist = list(sl)
    mainlist = list(ml)
    correct = 0
    for x in sublist:
        for y in mainlist:
            if x == y:
                mainlist.remove(y)
                correct += 1
                if correct == len(sublist):
                    return True
                break
    return False
say.server = 'Undertale'

@base.cacofunc
async def what(message, client):
    '''
    **{0}What** <was his name again?>
    Generates a name for uh... Fire... Hotsbro... You know, the guy from Hotland who was fire-based.
    *Example: `{0}What was his name again?`*
    '''
    if message.content.strip()[len(base.config['invoker']):].lower() == 'what was his name again?':
        heatsflames = [
            'Heats',
            'Flames',
            'Firey',
            'Hot',
            'Fire',
            'Hots',
            'Fires',
            'Flame',
            'Flamey',
            'Heaty',
            'Burning',
            'Char',
            'Charred',
            'Charry',
            'Burns',
            'Burn',
            'Blazes',
            'Blaze',
            'Blazing',
            'Ember',
            'Embers',
            'Arson',
            'Sparky',
            'Sparks',
            'Infernal',
            'Inferno',
            'Melt',
            'Melts',
            'Melty',
            'Melting',
            'Seary',
            'Searing',
            'Sear',
            'Swelter',
            'Sweltering',
            'Thermal',
            'Warm',
            'Roast',
            'Roasty',
            'Combustion',
            'Combustiony',
            'Broil',
            'Broils',
            'Broily',
            'Broiling',
            'Boil',
            'Boils',
            'Boily',
            'Boiling',
            'Warms',
            'Flaming',
            'Heating',
            'Warming',
            'Roasting',
            'Ignis',
            'Flameo',
            'Toast',
            'Potentia',
            'Toasts',
            'Toasting',
            'Toasty',
            'Lava',
            'Lavas',
            'Magma',
            'Magmas',
            'Stars',
            'Star',
            'Starry',
            'Grill',
            'Grilly',
            'Grilling',
            'Steam',
            'Steamy',
            'Steamer',
            'Steams',
            'Redhot',
            'Redhots',
            'Spicy',
            'Spice',
            'Spicing',
            'Fuming',
            'Fumes',
            'Blast',
            'Blasts',
            'Blasting',
            'Blaster',
            'Cinder',
            'Cinders',
            'Pyro',
            'Sizzling',
            'Sizzle',
            'Sizzler',
            'Sizzles',
            '~Wang Fire',
            '~That guy whose name I can\'t remember',
            '~That guy whose name I forgot',
            '~Firey Whatsisface',
            '~That guy who\'s made of fire, you know the one.',
            '~Mr. Burns',
            '~Steve',
            '~Red Hot Chibi Pepper',
            '~Mr. Hotpants McGee',
            '~SO EASILY DEFEATED',
            '~Grillby',
            '~JOHN CENA',
            '~Burnie Sanders',
            '~Mr. Explosion Man'
        ]
        person = [
            'man',
            'guy',
            'humanus',
            'dude',
            'face',
            'head',
            'waffle',
            'bro',
            'bud',
            'bub',
            'smith',
            'runt',
            'pip',
            'ton',
            'sir',
            'ster',
            'boy',
            'ius',
            'master',
            'kid'
        ]

        guesses = [
            ['Yeah, that was... uh... ', '?'],
            ['I\'m pretty sure his name was ', '.'],
            ['Oh yeah, that guy! That guy! ', '!'],
            ['Wasn\'t he called ', '?'],
            ['Yeah, I actually *remembered it*. It was ', '.'],
            ['You caught me at a bad time. Uh... ', '?'],
            ['It\'s on the tip of my tongue... Oh! ', '?'],
            ['Got it. Bam. ', '.'],
            ['Wait, lemme start Undertale really quickly to check- Oh man, I already passed him! Uh... Was it ', '?'],
            ['He\'ll never forget that I forgot it was ', '. I think.'],
            ['He\'ll always remember that I remembered it was ', '. I think.'],
            ['It\'s gotta be ', '. Definitely.'],
            ['', ', probably.'],
            ['', ', most likely.'],
            ['', '...'],
            ['Hmm, is iiiit... ', '?'],
            ['I\'m pretty sure that it was ', ', right?'],
            ['Who, the firey guy? ', '. I think.'],
            ['Grillby? Wait, no, ', '!'],
            ['That guy who\'s on fire with a star on him, right? Ah, that\'s ', '. I\'m sure of it!'],
            ['It has to be ', '. No doubt about it!'],
            ['Heats Flamesman? More like ', '!'],
            ['Everybody keeps getting his name wrong. We should all remember how it\'s ', '.'],
            ['Uh... ', '.'],
            ['That guy who asks you to remember his name? I forgot. My best guess is ', ', though.'],
            ['As *if* I\'d forget who ', ' was!'],
            ['$10 says it\'s ', '.'],
            ['$11 says it\'s ', '.'],
            ['$12 says it\'s ', '.'],
            ['$13 says it\'s ', '.'],
            ['$14 says it\'s ', '.'],
            ['$15 says it\'s ', '.'],
            ['$9 says it\'s ', '.'],
            ['$8 says it\'s ', '.'],
            ['$20 says it\'s ', '!'],
            ['$50 says it\'s ', '!'],
            ['I\'ll bet $100 that his name is ', '.'],
            ['$1 says it\'s ', '.'],
            ['I\'ll give you my entire life savings if it isn\'t ', '.'],
            ['You know what? I bet it\'s something stupid, like ', ' or something.'],
            ['It *could* be ', ', but you never know.'],
            ['', ', or I\'ll eat my hat.'],
            ['Jerry? No, wait, ', '.'],
            ['It can\'t be ', ', surely!'],
            ['It has to be ', ', surely!'],
            ['I\'d check, but I\'m at the core now. It\'s ', ' though, right?'],
            ['I\'ll always remember that name! He\'s ', '!'],
            ['Thankfully I got Undertale on my android, so I can check right now... Ah, ', '.'],
            ['Firey Ho- no, Toasty Sizzlewa- no, Mr. Poopybuttho- no... Ah, I give up. Just put his name down as ', ' and forget about it.'],
            ['What do you mean it isn\'t ', '!?'],
            ['Surely, his name is ', '?'],
            ['I give up, his name could be ', ' for all I care.'],
            ['I\'m never gonna give him up, let him down, or run around and forget that his name is actually ', '.'],
            ['**His name is** ', '​**!!!!!** 🎺🎺🎺🎺🎺'],
            ['Is this a joke? Are you having a giggle? Everyone knows that his name is ', '.'],
            ['Are you kidding, I even wrote a song about him! ♫ He is the best, who baffles all the rest, ', ' is his name, and being surprised is his game! ♫ You like it?'],
            ['Nope, sorry, I forgot his name. All I can remember is how he kept shouting ', ' over and over.'],
            ['When I told him his name was ', ', he asked how he could have been so easily defeated!'],
            ['Wanna hear a joke? Why did ', ' cross the road? …I don\'t know, really.']
        ]

        guess = random.choice(guesses)
        heats = random.choice(heatsflames)
        if heats[0] == '~':
            await client.send_message(message.channel, '{}**{}**{}'.format(
                guess[0],
                heats[1:],
                guess[1]
            ))
        else:
            flames = '~'
            while flames[0] == '~':
                flames = random.choice(heatsflames)
            man = random.choice(person)
            if '{} {}{}'.format(heats, flames, man) == 'Heats Flamesman':
                await client.send_message(message.channel, 'Wait, I actually know it! His name was *most definitely* **Heats Flamesman**!')
            else:
                await client.send_message(message.channel, '{}**{} {}{}**{}'.format(
                    guess[0],
                    heats,
                    flames,
                    man,
                    guess[1]
                ))
what.server = 'Undertale'
