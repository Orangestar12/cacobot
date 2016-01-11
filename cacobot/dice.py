import cacobot.base as base
import random, time

@base.cacofunc
def d(message, client, *args, **kwargs):
    '''
    **.d** <*x*>d<*y*>
    Rolls <*x*> dice with <*y*> sides.
    *Example: `.d 2d6`*
    '''
    try:
        params = message.content.split(' ')
        dice = int(params[1][:params[1].find('d')])
        sides = int(params[1][params[1].find('d')+1:])

        #Generate random numbers, append to list.
        rolls = []
        for x in range(0, dice):
            rolls.append(random.randint(1, sides))

        #If the list only has 1 die, just print that number.
        if len(rolls) == 1:
            yield from client.send_message(message.channel, '{}: {}'.format(message.author.mention, str(rolls[0])))

        #Otherwise, print the list, and the list's sum.
        else:
            yield from client.send_message(message.channel, '{}: {} | {} of possible {}'.format(
              message.author.mention,
              str(rolls),
              str(sum(rolls)),
              str(dice * sides)
            ))

    except IndexError:
        # user did not format command correctly
        yield from client.send_message(message.channel, '{}: You must specify the number of dice and the faces each dice has seperated with a d. For example: .d 1d6 rolls one six-sided die. .d 5d2 rolls 5 2-sided die.'.format(message.author.mention))
d.server = 'Dice'

@base.cacofunc
def roll(message, client, *args, **kwargs):
    '''
    **.roll**
    *This command was created for the /g/ server.*
    Generates an integer based on the current time. If the last two digits are equivalent, appends the message with 'check 'em!'
    *Example: `.roll`*
    '''

    # This was written by @NoKeksGiven. Give that guy a shout-out!
    num = str(round(int(round(time.time() * 100) % 100000000)))
    if num[-1] == num[-2]:
        yield from client.send_message(message.channel, '{}: {}, check \'em!'.format(message.author.mention, num))
    else:
        yield from client.send_message(message.channel, '{}: {}'.format(message.author.mention, num))
roll.server = '/g/'

@base.cacofunc
def choice(message, client, *args, **kwargs):
    '''
    **.choice** [*one*; *two*...]
    Randomly choses an option from a semicolon-seperated list.
    *Example: `.choice CacoBot is Life; CacoBot is Love`*
    '''

    choices = message.content.split(' ', 1)
    if len(choices) > 1:
        choices = choices[1].split(';')
        if len(choices) > 1:
            yield from client.send_message(message.channel, '{}: {}'.format(message.author.mention, random.choice(choices).strip()))
        else:
            yield from client.send_message(message.channel, ':no_entry_sign: {}: You have provided only one choice to select from.'.format(message.author.mention))
    else:
        yield from client.send_message(message.channel, ':no_entry_sign: {}: You have provided no choices'.format(message.author.mention))
choice.server = 'Dice'
