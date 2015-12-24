import cacobot.base as base
import discord, random, traceback, subprocess

# No comments. Fuck you.

@base.cacofunc
def goatnick(message, client, *args, **kwargs):
    '''
    **.goatnick**
    *This command was created for the Undertale server.*
    Generates a politically incorrect name for Asgore from a list.
    *Example: .goatnick*
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
        'Big Sad Goat Dad'
    ];
    yield from client.send_message(message.channel, '{}: Asgore "{}" Dreemurr'.format(message.author.mention, random.choice(asgore_nicks)))
goatnick.server = 'Undertale'

@base.cacofunc
def summon(message, client, *args, **kwargs):
    '''
    **.summon** [*monster 1*] [*monster 2*]...
    *This command was created for the Undertale server.*
    Prints the array of [*monster*]s's encounter texts. Provide as many encounters as you want, or leave it blank to summon a random one.
    *Example: .summon Papyrus Snowdrake*
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
    if message.content.strip() == '.summon':

        # Add spoilers unless spoiler-free channel
        if message.channel.is_private or message.channel.name not in ['torielshome', 'fanworks', 'workshop']:
            monsters.update(spoilers)

        # 1 in 8k chance to add hidden monsters to rotation
        if random.randrange(0, 8000) == 300:
            monsters.update(hidden)

        msg = '```\n' + monsters[random.choice(list(monsters))]

        # 1 in 1k chance to spawn Jerry
        monster = random.choice(list(monsters))
        if random.randrange(0, 1000) == 300:
            msg += '\nJerry came, too.'

        msg += '\n```'

        yield from client.send_message(message.channel, msg)

    elif message.content.strip() == '.summon list':
        if message.channel.is_private or message.channel.name not in ['torielshome', 'fanworks', 'workshop']:
            monsters.update(spoilers)

        monsters.update(hidden)

        yield from client.send_message(message.channel, 'List of Monster Codes:\n```\n{}\n```'.format(' '.join(sorted(list(monsters)))))

    else:
        cmd = message.content.split(' ')[1:]
        msg = []

        if message.channel.is_private or message.channel.name not in ['torielshome', 'fanworks', 'workshop']:
            monsters.update(spoilers)

        monsters.update(hidden)

        for x in cmd:
            for y in monsters:
                if x.lower() == y.lower():
                    msg.append(monsters[y])
            else:
                if x.lower() == 'jerry':
                    msg.append('Jerry came, too.')

        # Detect special cases

        # KK & Madjick: Mercenaries
        if issublist(['Madjick pops out of its hat!','Knight Knight blocks the way!'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Knight Knight blocks the way!'][0]
            msg.remove('Madjick pops out of its hat!')
            msg.remove('Knight Knight blocks the way!')
            msg.insert(save, 'Mercenaries emerge from the shadows.')

        # Pyrope & Pyrope: Double Davis
        if issublist(['Pyrope bounds towards you!','Pyrope bounds towards you!'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Pyrope bounds towards you!'][0]
            msg.remove('Pyrope bounds towards you!')
            msg.remove('Pyrope bounds towards you!')
            msg.insert(save, 'The rare and threatening Double Davis.')

        # Vulkin + Tsun: Jealous
        if issublist(['Tsunderplane gets in the way! Not on purpose or anything.','Vulkin strolls in.'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Tsunderplane gets in the way! Not on purpose or anything.'][0]
            msg.remove('Tsunderplane gets in the way! Not on purpose or anything.')
            msg.remove('Vulkin strolls in.')
            msg.insert(save, 'Tsunderplane attacks! Not because it\'s jealous Vulkin is paying attention to you.')

        # Vulkin + Vulkin: Strange Parade
        if issublist(['Vulkin strolls in.','Vulkin strolls in.'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Vulkin strolls in.'][0]
            msg.remove('Vulkin strolls in.')
            msg.remove('Vulkin strolls in.')
            msg.insert(save, 'A strange parade blocks the path.')

        # Aaron + Woshua: Easter Egg
        if issublist(['Aaron flexes in!','Woshua shuffles up.'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Aaron flexes in!'][0]
            msg.remove('Aaron flexes in!')
            msg.remove('Woshua shuffles up.')
            msg.insert(save, 'Woshua and Aaron appear.')

        # Snowdrake + Ice Cap: pose
        if issublist(['Snowdrake flutters forth!','Ice Cap struts into view.'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Snowdrake flutters forth!'][0]
            msg.remove('Snowdrake flutters forth!')
            msg.remove('Icecap struts into view.')
            msg.insert(save, 'Icecap and Snowdrake pose like bad guys.')

        # Loox + Veg/Migosp: loox & Co.
        if issublist(['Loox drew near!','Vegetoid came out of the earth!', 'Migosp crawled up close!'], msg) or issublist(['Loox drew near!','Vegetoid came out of the earth!'], msg) or issublist(['Loox drew near!', 'Migosp crawled up close!'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Loox drew near!'][0]
            msg.remove('Loox drew near!')
            try:
                msg.remove('Migosp crawled up close!')
            except:
                pass
            try:
                msg.remove('Vegetoid came out of the earth!')
            except:
                pass
            msg.insert(save, 'Loox and co. decided to pick on you!')

        # Two Moldsmal: Moldsmal and Moldsmal
        if issublist(['You tripped into a line of Moldmals.','You tripped into a line of Moldmals.'], msg):
            save = [i for i,x in enumerate(msg) if x == 'You tripped into a line of Moldmals.'][0]
            msg.remove('You tripped into a line of Moldmals.')
            msg.remove('You tripped into a line of Moldmals.')
            msg.insert(save, 'Moldsmal and Moldsmal block the way.')

        # Astig, FF, Whim: ULTRA-VIOLENCE
        if issublist(['Whimsalot rushed in!', 'Final Froggit was already there, waiting for you.','Eyes appeared from the shadows.'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Final Froggit was already there, waiting for you.'][0]
            msg.remove('Eyes appeared from the shadows.')
            msg.remove('Whimsalot rushed in!')
            msg.remove('Final Froggit was already there, waiting for you.')
            msg.insert(save, 'What a nightmare!')

        # Astig + FF: Not correct...
        if issublist(['Final Froggit was already there, waiting for you.','Eyes appeared from the shadows.'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Final Froggit was already there, waiting for you.'][0]
            msg.remove('Eyes appeared from the shadows.')
            msg.remove('Final Froggit was already there, waiting for you.')
            msg.insert(save, 'That doesn’t seem correct.')

        # Whimsalot + FF: Believe it?
        if issublist(['Final Froggit was already there, waiting for you.','Whimsalot rushed in!'], msg):
            save = [i for i,x in enumerate(msg) if x == 'Final Froggit was already there, waiting for you.'][0]
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
            yield from client.send_message(message.channel, '```\n{}\n```'.format('\n'.join(msg)))
        else:
            yield from client.send_message(message.channel, '{}: I could not find any valid monster codes in your query. Use .summon list to see them all.'.format(message.author.mention))
summon.server = 'Undertale'

@base.cacofunc
def determinate(message, client, *args, **kwargs):
    '''
    **.determinate** [color\=*color*] [font\=*font*] <*text*>
    *This command was created for the Undertale server.*
    Generates an image with text of your choice using the font Determination Mono. [color\=*color*] can be provided as a CSS color, like hexadecimal (#FF7700), rgb (rgb(255,128,0)), or color code (orange). [font=*font*] can be *sans*, *papyrus*, *wd*, or *ut*. Omit to leave it as DTM.
    You can also use colons instead of equals signs. If you specify a font not in our keys using underscores in place of spaces, you
    *Example: .determinate color=#0000FF font=Papyrus YOU'RE BLUE NOW! THAT'S MY ATTACK.*
    '''
    # The example used to be this:
    # *Example: .determinate color=#FF0000 Where are the knives.*
    # Then the spoiler rules got more strict so I had to change it.

    if message.content.strip() == '.say' or message.content.strip() == '.determinate':
        yield from client.send_message(message.channel, 'If you do not know how to use this command, call `.help determinate`!')
    else:
        color = '#FFFFFF'
        font = 'Determination Mono'
        strokewidth = '0'
        lineheight = 36 #This is actually slightly big for the height of lines but *Shrug*
        fontwidth = '28px'
        precedent = 32
        width = '640'

        # I'm basically only using this to quickly strip ".determinate" from the message
        TextToSay = message.content.split(' ', 1)[1]

        # find color
        if 'color=' in TextToSay.lower() or 'color:' in TextToSay.lower():
            index = TextToSay.find('color=') + 6
            end = TextToSay.find(' ', index)
            color = TextToSay[index:end]
            index = index - 6
            end = end + 1
            TextToSay = TextToSay[:index] + TextToSay[end:]

        if color == 'rainbow':
            # MEME STOPPER CODE #STOPMEMESNOW
            yield from client.send_message(message.channel, random.choice([
            'See, this is why we can\'t have nice things.',
            'It was Jerry, wasn\'t it. *He* put you up to this.',
            'Why don\'t you call your mother or something? It\'d be more productive than exhausting my list of snarky comments for when you post memes.',
            'Seriously, keep this up and nobody will love you.',
            'I think this counts as spam at this point.',
            '`* CacoBot is sparing you.`',
            'Can you just stop for a little while? That\'ll at least give me a second to wipe the tears from my eyes.',
            'You know what\'s going on here, don\'t you? You just wanted to see me suffer.',
            'You don\'t understand how it works down here, do you?',
            'You IDIOT.',
            'Was it something I did? Did *I* do something to make you do this?'
            ]))
        else:
            if color == 'RAINBOW':
                clr = ['#']
                for x in range(0, 6):
                    clr.append(random.choice('0123456789ABCDEF'))
                color = ''.join(clr)

            #find font
            if 'font=' in TextToSay.lower() or 'font:' in TextToSay.lower():
                index = TextToSay.find('font=') + 5
                end = TextToSay.find(' ', index)
                newfnt = TextToSay[index:end].lower()

                if newfnt == 'sans':
                    font = 'Comic Sans MS'
                    lineheight = 40
                elif newfnt == 'papyrus':
                    font = 'Papyrus'
                    strokewidth = '1'
                    fontwidth = '20px'
                elif newfnt == 'wd':
                    font = 'Wingdings'
                    strokewidth = '1'
                    fontwidth = '18px'
                    lineheight = 24
                elif newfnt == 'ut':
                    font = 'Monster Friend Fore'
                    width = '700'
                    precedent = 22
                else:
                    font = newfnt.replace('_', ' ')

                index = index - 5
                TextToSay = TextToSay[:index] + TextToSay[end:]

            TextToSay = TextToSay.strip()
            if font == 'Wingdings':
                TextToSay = TextToSay.upper()

            if TextToSay.startswith('* '):
                indent = True
            else:
                indent = False

            TextList = []

            while TextToSay:
                if indent == True:
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
                    try:
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
                #indent mode: detect "* "s
                for x in TextList:
                    if x.startswith('* '):
                        TextToSay += x + '\n'
                    else:
                        TextToSay += '  ' + x + '\n'
            else:
                # Not in indent mode: just join list
                TextToSay = '\n'.join(TextList)

            save = TextToSay
            TextToSay = htmlEntities(TextToSay)
            lines = len(TextList)
            height = (lines * lineheight) + 94

            svgString = r'<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg width="' + width + '" height ="' + str(height) + '" viewBox="0 0 ' + width + ' ' + str(height) + '" xmlns="http://www.w3.org/2000/svg" version="1.1" shape-rendering="optimizeSpeed"><rect width="100%" height="100%" fill="black"/>'

            # MFF requires no rect and a back layer.
            if font != 'Monster Friend Fore':
                svgString += '<rect width="576" height="' + str(height - 64) + '" x="33" y="33" stroke-width="6" stroke="white"/>'
            else:
                svgString += '<text fill="' + color + '" stroke="' + color + '" stroke-width="' + strokewidth + '" x="50" y="50" dy="' + fontwidth + '" font-size="' + fontwidth + '" font-family="Monster Friend Back" xml:space="preserve" opacity="0.65">' + TextToSay + '</text>'

            svgString += '<text fill="' + color + '" stroke="' + color + '" stroke-width="' + strokewidth + '" x="50" y="50" dy="' + fontwidth + '" font-size="' + fontwidth + '" font-family="' + font + '" xml:space="preserve">' + TextToSay + '</text></svg>'

            # write svg
            with open('tmp.svg', 'w') as data:
                data.write(svgString)

            # requires imagemagick
            subprocess.check_call(['convert', 'tmp.svg', 'tmp.png'])

            yield from client.send_file(message.channel, 'tmp.png')

            # Try to delete the message.
            try:
                yield from client.delete_message(message)
            except (discord.Forbidden, discord.HTTPException):
                # do nothing if no permission or message
                pass

            # send msg if wingdings
            if font == 'Wingdings':
                yield from client.send_message(message.channel, '*{}*'.format(save))

            # send author
            yield from client.send_message(message.channel, '*Sent by {}.*'.format(message.author.mention))
determinate.server = 'Undertale'

# You know, while I'm here, here's the StackOverflow post that has the function.
# It's really useful. Credit where it's due.
# http://stackoverflow.com/questions/18609778/solved-python3-convert-all-characters-to-html-entities
def htmlEntities( string ):
    return ''.join(['&#{0};'.format(ord(char)) for char in string])

@base.cacofunc
def forebode(message, client, *args, **kwargs):
    '''
    **.forebode** [*mention*]
    *This command was created for the Undertale server. Just for Felarine. ;)*
    This is a shortcut to add the "Foreboden" role to a user. If your server has no
    "Foreboden" role, this will fail.
    *Example: .forbode @CacoBot*
    '''
    if message.channel.permissions_for(message.author).can_manage_roles:
        try:
            foreboden = discord.utils.find(lambda m: m.name == 'Foreboden', message.server.roles)
            if foreboden != None:
                for ment in message.mentions:
                    yield from client.replace_roles(ment, foreboden)
                    yield from client.send_message(message.channel, '{}: That person has been foreboden.'.format(message.author.mention))
            else:
                yield from client.send_message(message.channel, '{}: You must create a role named \'Foreboden\' before you can use this command.'.format(message.author.mention))
        except:
            yield from client.send_message(message.channel, '{}: I do not have the permission to perform this command yet.'.format(message.author.mention))
    else:
        yield from client.send_message(message.channel, '{}: You do not have the permission to manage roles.'.format(message.author.mention))
forebode.server = 'Undertale'

@base.cacofunc
def say(message, client, *args, **kwargs):
    '''
    **.say** [*params*]
    A shorcut to .determinate.
    '''
    yield from determinate(message, client, args, kwargs)

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
