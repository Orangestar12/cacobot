import random
import urllib.request

import cacobot.base as base

# boris.slipgate.org seems to be misconfigured. I'm sure it'll be fixed
# eventually. Until then, this command is disabled.

# @base.cacofunc # Uncomment to reenable.
async def wadidea(message, client):
    '''
    **{0}wadidea**
    *This command was created for the /vr/ Doom server.*
    Generates a wad idea from boris.slipgate.org.
    *Example: `{0}wadidea`*
    '''

    #Download the file.
    result = urllib.request.urlopen('http://boris.slipgate.org/?a=mapgen').read().decode('ISO-8859-1')

    #The webpage will always have this line where the idea begins:
    start = int(result.find('<table align="center" width="400"><tr><td>'))
    start += 42
    #...and this where it ends.
    end = int(result.find('</td></tr></table>\n<hr width="95%">'))

    #Since that's all we're interested in, we make a new var with just that.
    result = result[start:end].strip()

    #Next, we remove all <br>s and line breaks.
    result = result.replace('<br>\n', ' ')

    await client.send_message(message.channel, '{}: {}\n\n*Provided by boris.slipgate.org/?a=mapgen*'.format(message.author.display_name, result))
    return
wadidea.server = 'Doom'

@base.cacofunc
async def fortune(message, client):
    '''
    **{0}fortune**
    Generates a random fortune from a list.
    *These quotes are from the mod DemonSteele by TerminusEst13. Many are from Shadow Warrior and Shadow Warrior 2013. Thanks for lettin' me use em, Term!*
    *Example: `{0}fortune`*
    '''
    fortunes = [
        'If you want to blow someone\'s mind, consider hollow-point .45s.',
        'Consider the horse. No, seriously. Weird damn animals.',
        'Don\'t fry bacon in the nude.',
        'The world may be your oyster, but you\'ll probably never get its pearl. Sorry.',
        'When life gives you lemons, that means you have more than one lemon. It\'s plural, you see. It\'s an X+1 amount of lemons. It was probably a gift.',
        'When you squeeze an orange, orange juice comes out. Because that\'s what\'s inside. Duh.',
        'I don\'t know. Ask your mom.',
        'Great misfortune will befall you. Blame it on lag.',
        'Constant grinding can turn an iron rod into a needle, or you might just be dry-humping.',
        'Shit happens when you party naked.',
        'You are not illiterate.',
        'What the fuck did you just fucking say about me, you little bitch?',
        'You should kill all business associates.',
        'Roses are red, violets are blue, I was written in black ink.',
        'Life is like a car that won\'t slow down. Them\'s the brakes.',
        'A good bullet is like an easy copier. Hitscan.',
        'Fortune cookies aren\'t actually Chinese. They\'re a take on the Japanese "o-mikuji senbei", a sweet cracker with a little slip of paper tucked in. Japanese-American immigrants in the 19th century sold them to Chinese restaurants.',
        'Only listen to the fortune cookie. We are your friends. Everyone else lies to you.',
        'Never give up. Unless defeat arouses that one girl in accounting.',
        'Some fortune cookies contain no fortune.',
        'Today is a huge improvement over yesterday. Probably.',
        'You will recieve a fortune sometime in your future.',
        'You will be hungry again in one hour.',
        'You\'re probably thinking, "Geeze, I could write better fortunes than that", right? Well, screw you, I have like a hundred to write.',
        'I have become circus2.wad, destroyer of servers.',
        'Is it wrong to fap to your ex?',
        'Life sucks, unless you wear a bikini and show off.',
        'It\'s a shame to see someone like you boarding the jelly train.',
        'Your opinions are fucking shit and they are also wrong.',
        'A lot of people say money doesn\'t lead to happiness, but I haven\'t seen them give their money away.',
        'It takes only a word to turn away wrath. For best results, try screaming it in anger.',
        'It takes many nails to build a crib, but only one screw to fill it.',
        'Confuscius say: Think for your own damn self.',
        'Do not despise the racketeer. Instead, despise his sport.',
        'The only acceptable place to take cover is behind a wall of bullets.',
        'Reloading is just foreplay for your gun.',
        'Taking credit for other people\'s work is the cool way to get ahead.',
        'They call it a bloodbath but you really can\'t clean anything with it.',
        'Opening up people is like finding secret doors. Approach casually and UNF until it works.',
        'Cut a demon in half? Whoa there, tough guy. Better put that on your resume.',
        'Words left unspoken lead to regret and self doubt. Try posting angrily about it online.',
        'Your erotic attack is successful. Roll 6d9s.',
        'Why was six afraid of seven? It wasn\'t. They\'re symbols representing established numerical values. They don\'t feel fear.',
        'What\'s brown and sticky? A stick.',
        'OH NO DON\'T LOOK I\'M NAKED',
        'I\'d say red is your color, but in Korea red is the color of masculinity.',
        'This is my sword, this is my gun. One is for killing, the other is for...well, also for killing, I guess.',
        'You don\'t need a parachute to skydive. You need a parachute to skydive twice.',
        'You will be attacked by demons.',
        'No one ever died of a broken heart. But a sword shoved straight into it? Not gonna lie. That\'s killed a couple people.',
        'It\'s not drowning, it\'s just putting breathing on Hard Mode.',
        'If you\'re hungry, eat it. If it\'s cute, fuck it. If it\'s a problem, whip it.',
        'Chicks dig swole pythons. Feed your pet snakes way too much!',
        'You not Lo Wang. You No Wang.',
        'When Navi speaks, use (^) to listen well to her words of wisdom...',
        'Call Apogee, say Aardwolf.',
        'You can make your own happiness. In a meth lab.',
        'Face facts with dignity and also a sword and a plethora of heaven-blessed firearms.',
        'Adversity is the parent of virtue. Insisting on UV-ing Hell Revealed is the parent of stupidity.',
        'Sometimes the best part of the journey is not the destination, but laying waste to the demon waiting at the destination.',
        'Watashi no hobakurafuto wa unagi de ippai desu.',
        'Let your deeds speak for themselves. Your flashy special combo moves can do the bragging.',
        'You will always be surrounded by your true friends. Yes, the guys shooting at you. They\'re your friends now.',
        'Phew! About goddamn time I got out of that cookie.',
        'IT\'S A SECRET TO EVERYBODY.',
        'You will take a pleasant journey to a place far away, just as soon as you can find the secret exit.',
        'You believe in the goodness of mankind... but you have an internet connection?!',
        'You will live long and enjoy life. Unless you get shot by demons. But what are the odds of that?',
        'Someday, you\'ll look back on this and laugh nervously before changing the topic.',
        'Mama-say mama-sah ma-ma-coo-sah.',
        'Your skeleton lurks inside of you, waiting patiently.',
        'Seven days.',
        'I know what you did last summer.',
        'Caleb is never going to be added to Samsara.',
        'Strifeguy is never going to be added to Samsara.',
        'Love will lead the way. So will IDDT.',
        'Look to La Luna!',
        'Buy Major Stryker.',
        'Seeing is believing, unless your SAN stat is 0.',
        'You\'ll get your own sprite set someday.',
        'The best is yet to come. Unless you cheated and got the best from the start, in which case, welp.',
        'You just don\'t talk shit about another man\'s waifu.',
        'Believe in yourself. The rest of us think you\'re an idiot.',
        'Pain may be weakness leaving the body, but you\'ve got so much to give.',
        'Fighting for peace may be an oxymoron, but it\'s more fun than the alternative.',
        'A wise man once said, it is not enough to settle for mediocrity. You must git gud, scrub.',
        '404: Fortune not found. Try again later.',
        'I refuse to do anything productive today.',
        'Axes take skill.',
        'Everything\'s more fun when you\'re drunk.',
        'Study finds OP still sucking cock on a regular basis.',
        '99 glitches in the code on the wall, 99 glitches in the code. Take one down, patch it around, 142 glitches in the code on the wall.',
        'Justice fears no skelly!',
        'When tempted to fight fire with fire, remember that the Fire Department usually uses water.',
        'If what you don\'t know can\'t hurt you, you\'re invulnerable.',
        'Patience and a kind word can take care of most situations, but so can a bullet.',
        'One of these days, the enemies will learn how to respawn. Then we\'ll all be fucked.',
        'In the time it took for DemonSteele to start development, enter alpha/beta, get a full weaponset, tons of new sprites, a full quote roster, be released, and win a Cacoward, Space Pirate still has not updated.',
        'I should not be spending thirty goddamn minutes thinking up one single message.',
        'How is eating fried chicken like being in Hell? Thigh flesh consumed.',
        'This is just like one of my Korean manhwas!',
        'At some point, you will be the next person on Earth to die.',
        'Wow, your browser history is kind of weird.',
        'Today\'s forecast: Not fucking going outside.',
        'What do you do with an epileptic lettuce? Make a seizure salad.',
        'Never trust an acupuncturist. They\'re back-stabbers.',
        'system error 0xfded',
        'If you think food has all the answers, you must be fat as hell.',
        'Senpai noticed me!',
        'I want to be inside you but nobody ever eats the paper. ;_;',
        'I\'d ask you to be gentle with me but you seem to have already snapped me in half.',
        'Leather armor is the best for sneaking, because it\'s made of Hide.',
        'Excuse me, do you have a moment free to talk about our lord and savior, Jesus Christ?',
        'I sure hope I\'m not supposed to be guarding the Spear of Destiny right now.',
        'I bet the UAC did this.',
        'Does this run with Brutal Doom?',
        'I\'m surprised you can read this, what with the firing and shooting and running around at 50 MPH.',
        'Mom can\'t make you clean your room.',
        'Did you know that you can drink lava? Only once, though.',
        'Go to Heaven for the men, but go to Hell for the women.',
        'Gomen nasai. Nihongo ga kakenai.',
        'Let me tell you why Satan is a myth and the demons are actually aliens.',
        'Hae-Lin is actually really bad at poker, because she folded 1000 times.',
        'Why bother with original content when you can just quote a meme and have an epic win?',
        'John Who? John Woo.',
        'Install your GPU drivers.',
        'You think I have it rough? Wait until you see my friend, the New Year\'s Party Popper.',
        'Did you know that dumb upside down is qnwp?',
        'A person dies every 11 seconds. How many people have died since you started?',
        'I\'ve never seen a Kano transformation.',
        'Beware of he who would deny you access to information, for in his heart he dreams himself your master.',
        'I\'d say it\'s a good day to die, but next Sunday might be good too.',
        'Control the media, control the mind.',
        'You\'re not the boss of me!',
        'There\'s absolutely no illuminati watching you right now.',
        'Protip: To kill the DevilDriver, stab it until it dies.',
        'play some punch out with these nerds and beat them 2 the punch',
        'How exactly do you refine toxins?',
        'HOW DOE\'S IT FEEL TO BE WELL DONE? BUT I BET YOU TASTE TERRIBLE.',
        'Boy, this mod would be so much better if it had its own dedicated mapset.',
        'What\'s the speed of dark?',
        'Does this run with HDoom?',
        'Let me tell you about my fetishes.',
        'Lewd.',
        'Bang.',
        'Remember, ironic shitposting is still shitposting.',
        'Behold, I have created the smith that bloweth the coals in the fire and that bringeth forth an instrument for this work; and I have created the waster, to destroy.',
        'I looked, and there was a pale horse! Its rider\'s name was Death, and Hell followed him. They were given authority over one-fourth of the earth to kill people using wars, famines, plagues, and the wild animals of the earth.',
        '**DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO DOO**',
        'The only thing better than a delicious cake is a delicious cake on fire.',
        'Your difficulties will strengthen you. Or break you. One of the two.',
        'Remember your love, for hate is never conquered by hate; hate is conquered by love. Both are kind of flimsy against a .45, though.',
        'The Great Wall wasn\'t built in one day. The Berlin Wall was, though.',
        'We cannot direct the wind, we can only adjust the sails. You\'re fucked either way if it\'s a typhoon, though.',
        'Great thoughts come from the heart. So do stupid decisions.',
        'When you cannot feel happy, working with a smile may rub off happiness on others. Or take pills. Pills are easier.',
        'You will enjoy good health. Until you die.',
        'There is no love so pure and passionate as the love of oneself. Just don\'t do it in public. Ew.',
        'They say "May your dreams come true", but how many of your dreams aren\'t weird shit?',
        'Do you really think you\'ll find deep philosophical meaning from a little slip of paper inside a cookie?',
        'For twelve years you\'ve been asking "Who is John Galt?" This is John Galt speaking. I\'m the man who\'s taken away your victims and thus destroyed your world. You\'ve heard it said that this is an age of moral crisis and that Man\'s sins are destroying the world. But your chief virtue has been sacrifice, and you\'ve demanded more sacrifices at every disaster. You\'ve sacrificed justice to mercy and happiness to duty. So why should you be afraid of the world around you? Your world is only the product of your sacrifices. While you were dragging the men who made your happiness possible to your sacrificial altars, I beat you to it. I reached them first and told them about the game you were playing and where it would take them. I explained the consequences of your "brother-love" morality, which they had been too innocently generous to understand. You won\'t find them now, when you need them more than ever. We\'re on strike against your creed of unearned rewards and unrewarded duties. If you want to know how I made them quit, I told them exactly what I\'m telling you tonight. I taught them the morality of Reason – that it was right to pursue one\'s own happiness as one\'s principal goal in life. I don\'t consider the pleasure of others my goal in life, nor do I consider my pleasure the goal of anyone else\'s life. I am a trader. I earn what I get in trade for what I produce. I ask for nothing more or nothing less than what I earn. That is justice. I don\'t force anyone to trade with me; I only trade for mutual benefit. Force is the great evil that has no place in a rational world. One may never force another human to act against his/her judgment. If you deny a man\'s right to Reason, you must also deny your right to your own judgment. Yet you have allowed your world to be run by means of force, by men who claim that fear and joy are equal incentives, but that fear and force are more practical. You\'ve allowed such men to occupy positions of power in your world by preaching that all men are evil from the moment they\'re born. When men believe this, they see nothing wrong in acting in any way they please. The name of this absurdity is "original sin". That\'s inmpossible. That which is outside the possibility of choice is also outside the province of morality. To call sin that which is outside man\'s choice is a mockery of justice. To say that men are born with a free will but with a tendency toward evil is ridiculous. If the tendency is one of choice, it doesn\'t come at birth. If it is not a tendency of choice, then man\'s will is not free.',
        'You have selected Microsoft Sam as the computer\'s default voice.',
        'What\'s the smallest amount of money you would reach into a toilet to get?',
        'Hey girl, let\'s turn this bouncy house into a bouncy home.',
        'I want a lady in the streets and a lady in the sheets. I want a lady covering the exits, one watching the car park, and one sniping from the roof.',
        'I\'m getting worried, my boomerang should have been back hours ago.',
        'Son, I\'m sorry you heard your mother and I fighting. But she\'s got a long way to go before she faces the Undertaker at Wrestlemania.',
        'Whoever named them missiles wasn\'t very optimistic.',
        'Gun safety helps save foolish lives. That\'s why God invented knives. Burma shave.',
        'A balanced person gives as good as they get. Don\'t do that. You\'re killing people, here.',
        'Say it with flowers. Daisy cutters count.',
        'I\'ll call you back, Cheryl, someone is rudely interrupting my alone time.',
        'FWD: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: URGENT',
        'The lottery gives you about a 1 in 200 million chance you won\'t be going to work tomorrow. Alcohol will give you a 1 in 5.',
        'No. Of course I\'m not mad. It\'s fine. It\'s fine!',
        'For a really awkward time, call me.',
        'If you love someone, poison them a little bit each day. If they don\'t suspect you at all, they might be the one.',
        'If you love them, set them free. If you REALLY love them, amputate limbs for your own personal memento.',
        'Sixteen men on a dead man\'s chest is how I\'m gonna start my next yaoi fanfiction.',
        'Lose weight fast! See our associate Revenants for more details!',
        'So is it pronounced gibs or jibs?',
        'Hate. Let me tell you how much I\'ve come to hate you since I began to live.',
        'SMUG INTELLECTUAL. Formerly-rampant human-coded AI with a sense of humor seeks bipedal oxygen-breathing cyborg for serious relationship in the galactic core. I\'ve got cool guns if you like to break stuff. No yuppies. MRa2572 (5/23).',
        'do you like me y/n',
        'I dunno why people think you\'re into marrying Sue. Who even is Sue?',
        'Not now, I have a headache.',
        'Why is an angry drunk not called mean-spirited?',
        'Is this the real life? Is this just fantasy?',
        'I fell into a burning ring of fire, I went down down down and the flames went higher.',
        'It\'s a long way to the top, if you wanna rock n\' roll.',
        'Take your flame, ignite the world.',
        'I am not a number. I am a free man!',
        'I understand about indecision, but I don\'t care if I get behind. People living in competition, all I want is to have my peace of mind.',
        'If you choose not to decide, you still have made a choice.',
        'Congratulations. You\'ve just decoded the secret message. Please send your answer to Old Pink, in care of the Funny Farm.',
        'Good girls get their kicks after six.',
        'Acquire proficiency.',
        'Gee, I sure hope nothing blows up.',
        'Baka.',
        'Nope. Can\'t think of anything. Sorry.',
        'There is no cookie.',
        'Having sex is like playing bridge. If you don\'t have a good partner, you\'d better have a great hand.',
        '**HISSSSSSSSSSSSS**',
        'Man who lie on elevator, wrong on many levels.',
        'Hey, I\'m Grump.',
        'Work hard, die young, win valuable prizes!',
        'His name is Robert Paulson.',
        'Every time I put a reference in this list, God kills a kitten.',
        'I am a nihilist I believe in nothing.',
        'Killing me won\'t bring back your honey.',
        'Go Team Edward!',
        r'\*dramatic pause\*',
        'Better not tell you now.',
        'Outlook good.',
        'Good luck.',
        'Guys, the thermal drill, go get it.'
    ]
    # most of these are from https://github.com/TerminusEst13/Folded1000Times/blob/940b824a071f4a8298d6426be406725374355825/pk3/acs/weeb_const.h

    await client.send_message(message.channel, '{}: **FORTUNE SAY**:\n{}'.format(message.author.display_name, random.choice(fortunes)))
fortune.server = 'Doom'

@base.postcommand
async def doomthree(message, client):
    if message.author.id != client.user.id:
        if ('doom3' in message.content.lower() or 'doom 3' in message.content.lower()) and random.randint(1, 20) == 1:
            await client.send_message(message.channel, '**WHO TURNED OUT THE LIGHTS?**')
