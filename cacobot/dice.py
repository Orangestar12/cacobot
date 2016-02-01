import cacobot.base as base
import random, os

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

        if dice > 999 or sides > 999:
            yield from client.send_message(message.channel, ':no_entry_sign: One of your commands had more than three digits. I must ask you to limit this roll.')
        else:


            #Generate random numbers, append to list.
            rolls = []
            for x in range(0, dice):
                rolls.append(random.randint(1, sides))

            #If the list only has 1 die, just print that number.
            if len(rolls) == 1:
                yield from client.send_message(message.channel, '{}: {}'.format(message.author.mention, str(rolls[0])))

            #Otherwise, print the list, and the list's sum.
            else:
                msg = '{}: {} | {} of possible {}'.format(
                  message.author.mention,
                  str(rolls),
                  str(sum(rolls)),
                  str(dice * sides)
                )

                if len(msg) > 2000:
                    yield from client.send_message(message.channel, 'The result for that roll ended up being more than 2000 characters, so I couldn\'t send it.')
                else:
                    yield from client.send_message(message.channel, msg)

    except (IndexError, ValueError):
        # user did not format command correctly
        yield from client.send_message(message.channel, '{}: You must specify the number of dice and the faces each dice has seperated with a d. For example: .d 1d6 rolls one six-sided die. .d 5d2 rolls 5 2-sided die.'.format(message.author.mention))

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

@base.cacofunc
def later(message, client, *args, **kwargs):
    '''
    **.later**
    Posts a Spongebob title card referring to a later time.
    *Example: `.later`*
    '''
    pics = os.listdir('later')
    yield from client.send_file(message.channel, 'later/' + random.choice(pics))
