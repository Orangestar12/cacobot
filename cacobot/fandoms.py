import random
import re

import discord
import cacobot.base as base

@base.cacofunc
async def limbo(message, client):
    '''
    **{0}limbo** [*mention*]
    *This command was created for the Vocaloid server. Just for Rodea. ;)*
    This is a shortcut to add the "Limbo" role to a user. If your server has no "Limbo" role, this will fail.
    *Example: `{0}limbo @CacoBot`*
    '''
    if message.channel.permissions_for(message.author).ban_members:
        try:
            foreboden = discord.utils.find(lambda m: m.name == 'Limbo', message.server.roles)
            if foreboden != None:
                for ment in message.mentions:
                    await client.replace_roles(ment, foreboden)
                    await client.send_message(message.channel, '{}: {} has been Limbo\'d.'.format(message.author.mention, ment.name))
            else:
                await client.send_message(message.channel, '{}: You must create a role named \'Limbo\' before you can use this command.'.format(message.author.mention))
        except discord.Forbidden:
            await client.send_message(message.channel, '{}: I do not have the permission to perform this command yet.'.format(message.author.mention))
    else:
        await client.send_message(message.channel, '{}: You do not have the permission to manage roles.'.format(message.author.mention))



@base.cacofunc
async def ship(message, client):
    '''
    **{0}ship** [ list | *category* | *groups* ]
    Generates a random ship. Provide any amount of lists, or use *all* to mix them all together. Use `{0}ship list` to get a list of all existing lists and groups to ship, or use `{0}ship list [list]` to get DMed a list of all of the characters in that list.
    *Example: `{0}ship utmain gfsubsub`*
    '''
    ships = {
        'utmain' : [
            'Toriel',
            'Asgore',
            'Sans',
            'Papyrus',
            'Undyne',
            'Alphys',
            'Mettaton',
            'Muffet',
            'Napstablook',
            'Dogamy',
            'Dogaressa',
            'Temmie',
            'Grillby',
            'Burgerpants',
            'Catty',
            'Bratty',
            'Nice Cream Guy',
            'RG 01',
            'RG 02',
            'Doggo',
            'Snowdin Shopkeeper',
            'Frisk',
            'Chara',
            'Asriel',
            'Monster Kid',
            'Gaster',
            'Flowey',
            'Adult / Edgy / All 7 Souls Asriel',
            'Gerson',
            'Outertale!Sans',
            'Scientist!Sans',
            'Aftertale!Sans',
            'Error!Sans',
            'Underfell!Sans',
            'Underswap!Sans',
            'Sanzyfresh',
            'Reapertale!Sans',
            'Heats Flamesman',
            'Lesser Dog',
            'Greater Dog',
            'River Person',
            'Ruins Dummy',
            'Mad Dummy',
            'Annoying Dog',
            'Onionsan'
        ],
        'utminor' : [
            'Froggit',
            'Whimsun',
            'Loox',
            'Vegetoid',
            'Migosp',
            'Moldsmal',
            'Snowdrake',
            'Ice Cap',
            'Gyftrot',
            '*Jerry*',
            'Aaron',
            'Woshua',
            'Moldbygg',
            'Shyren',
            'Vulkin',
            'Tsunderplane',
            'Pyrope',
            'So Sorry',
            'Final Froggit',
            'Whimsalot',
            'Astigmatism',
            'Madjick',
            'Knight Knight',
            'Glyde',
            'Bird that carries you across a disproportionately small gap',
            'The "Thaaaaaat\'s Politics!" Bear',
            'The Crazy Bun in Grillby\'s',
            'Ragel, the "Mushroom Dance" mushroom',
            'Teeth Monster in Grillby\'s',
            'Snowdin Snowman'
        ],
        'gfmain' : [
            'Dipper',
            'Mabel',
            'Wendy',
            'Stan',
            'Ford',
            'Soos',
            'Candy',
            'Grenda',
            'Pacifica'
        ],
        'gfsub' : [
            'Rumble McSkirmish',
            'Dippy Fresh',
            'Tambry',
            'Tyrone',
            'Robbie',
            'Melody',
            'Xyler',
            'Craz',
            'Old Man McGucket',
            'Chutzpar the Manotaur',
            'Gideon',
            'Shandra Jimenez',
            'Summerween Trickster',
            '.GIFfany',
            'Sheriff Blubs',
            'Deputy Durland',
            'Tad Strange',
            'Marius',
            'Nate',
            'Lazy Susan',
            'Tambry',
            'Preston',
            'Bud Gleeful',
            'Lolph',
            'Dundgren',
            'Thompson',
            'Probabilitor',
            'Greggy C.',
            'Leggy P.',
            'Chubby Z.',
            'Creggy G.',
            'Deep Chris',
            'Wax Stan',
            'Jeff the Gnome',
            'Schmebulock',
            'Multibear',
            'Toot Toot McBumbersnazzle',
            'Poolcheck',
            'Paper Jam Dipper',
            'Summerween Trickster',
            'Toby Determined',
            'Manly Dan',
            'Tyler “Geeet ‘Em!” Cutebiker',
            'Nathaniel Northwest',
            'Priscilla Northwest',
            'Gabe Benson',
            'Agent Trigger',
            'Justin Kerprank',
            'Mermando',
            'Darlene the Spider Person',
            'Franz the Lilliputtian',
            'Aoshima',
            'The Love God',
            'The Hand Witch'
        ],
        'gfsubsub' : [
            'Big Henry the Lilliputtian',
            'Polly the Lilliputtian',
            'Wax Larry King’s Head',
            'Tats',
            'Thistle Downe',
            'Norman',
            'Steve the Gnome',
            'Carson the Gnome',
            'Jason the Gnome',
            'Mike the Gnome',
            'Andy the Gnome',
            'Tate McGucket',
            'Ghost Eyes',
            'That guy who married a woodpecker',
            'The Mattress King',
            'Sergei',
            'Emma Sue',
            'Pyronica',
            'Xanthar',
            'Paci-Fire',
            'The shapeshifter',
            '8-Ball',
            'Celestabellebethabelle',
            'Dipper Clone #3',
            'Dipper Clone #4',
            'Kryptos',
            'Hectorgon',
            'Teeth',
            'Keyhole',
            'The Hide Behind',
            'That Horrifying Sweaty “Get in my mouth” One-armed head voiced by Louis C.K.',
            'Testosteraur the Manotaur',
            'Pubertaur the Manotaur',
            'Pituitaur the Manotaur',
            'Leaderaur the Manotaur',
            'Beardy the Manotaur',
            'Clark the Manotaur',
            'Judge Kitty Kitty Meow Meow Face-Schartzstein',
            'Gremlobin',
            'Cyclocks',
            'The Candy Monster',
            'C-3-lhu'
        ],
        "gfquestionable" : [
            'Bill Cipher',
            'Waddles',
            'Blendin',
            'Abuelita',
            'Gompers the Goat',
            'Time Baby',
            'Quentin Trembley',
            'Mayor Befuttlefumpter',
            'The Northwest Dog',
            'The Gobblewonker',
            'Jerry.',
            'The robot that only faces left',
            'Octavia the 8-legged cow',
            'Thing #268',
            'The Pterodactyl',
            'The Footbot',
            'Bigfoot',
            'Shimmery Twinkleheart',
            'Clay Cyclops',
            'Dipper Clone #7'
        ],
        'jt' : [
            'Jon "JonTron" Jafari',
            'Arin "Egoraptor" Hanson',
            'Ethan "h3h3" Klein',
            'Grimbo',
            'Jacques',
            'Spaghetti',
            'Rockington',
            'George Lucas',
            'The Kool-Aid Man',
            'Duffy The Talking Cat!?!',
            'Macaulay Culkin',
            'Malkovich',
            'Giorgio Armani',
            'Daniel "Danny Sexbang" Avidan',
            'Natalia the Rancour',
            'Blueboobs McFurrydream',
            'Bootleg Michael Jackson',
            'Cinnamon (#1 Drowned Bird)',
            'Fred Durst',
            'Bootleg Michael Jackson'
        ]
    }
    groups = {
        'ut' : [
            'utmain',
            'utminor'
        ],
        'gf' : [
            'gfmain',
            'gfsub',
            'gfsubsub',
            'gfquestionable'
        ]
    }
    listToChooseFrom = []
    if len(message.content.split()) > 1:
        lists = message.content.lower().strip().split()[len(base.config['invoker']):]
        if lists[0] == 'list':
            if len(lists) > 1 and lists[1] in ships:
                await client.send_message(message.author, ', '.join(ships[lists[1]]))
            else:
                await client.send_message(message.channel, 'Available Lists:\n{}\n\nAvailable Groups:\n{}'.format(', '.join(ships), ', '.join(groups)))
        elif lists[0] == 'all':
            for x in ships:
                listToChooseFrom += ships[x]
            await client.send_message(message.channel, '**{}** x **{}**'.format(random.choice(listToChooseFrom), random.choice(listToChooseFrom)))
        else:
            unrecognized = []
            for x in lists:
                if x in ships:
                    listToChooseFrom += ships[x]
                elif x in groups:
                    for y in groups[x]:
                        listToChooseFrom += ships[y]
                else:
                    unrecognized.append(x)
            if listToChooseFrom:
                send = '**{}** x **{}**'.format(random.choice(listToChooseFrom), random.choice(listToChooseFrom))
                if unrecognized:
                    if len(unrecognized) == 1:
                        send = '*Removing unrecognized list: {}*\n'.format(unrecognized[0]) + send
                    else:
                        send = '*Removing unrecognized lists: {}*\n'.format(', '.join(unrecognized)) + send
                await client.send_message(message.channel, send)
            else:
                await client.send_message(message.channel, ':no_entry_sign: You did not provide enough valid lists to choose from.')

    else:
        await client.send_message(message.channel, ':no_entry_sign: {} You did not provide enough valid lists to choose from.'.format(message.author))

ohwhitelist = [
    '152821755164098561', # remove soon
    '149167686159564800',
    '143896176213622784'
]

@base.postcommand
async def oh(message, client):
    if message.author.id != client.user.id and (message.channel.is_private or message.server.id in ohwhitelist) and re.sub(r'[^a-z0-9 ]', '', message.content.lower()) == "oh" and random.randint(1, 10) == 1:
        await client.send_message(message.channel, 'oh')
