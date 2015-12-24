import cacobot.base as base
import math, random, subprocess

# Math, for polar2cartesian
# Random to get random colors and such
# Subprocess to call imagemagick (convert)

def htmlEntities( string ):
    return ''.join(['&#{0};'.format(ord(char)) for char in string])

# These are Discord's role colors.
colors = [
    '#1abc9c', # CYAN
    '#2ecc71', # GREEN
    '#3498db', # BLUE
    '#9b59b6', # PURPLE
    '#f1c40f', # YELLOW
    '#e67e22', # ORANGE
    '#e74c3c', # RED
    '#95a5a6', # GREY
    '#7f8c8d', # DARK_GREY
    '#34495e', # NAVY_BLUE
    '#11806a', # DARK_CYAN
    '#1f8b4c', # DARK_GREEN
    '#206694', # DARK_BLUE
    '#71368a', # DARK_PURPLE
    '#c27c0e', # STRONG_ORANGE
    '#a84300', # DARK_ORANGE
    '#992d22', # DARK_RED
    '#979c9f', # DARK_GREY_BLUE
    '#bcc0c0', # LIGHT_GREY
    '#2c3e50'  # DARK_NAVY_BLUE
]

def polar2cartesian(centerX, centerY, radius, angleInDegrees):
    '''
    Generate a tuple of cartesian coordinates from polar ones.

    This was originally some JS code posted on StackOverflow because I failed
    geometry too many times. I have adapted it for use in Python. The original
    code is here:
    http://stackoverflow.com/questions/5736398/how-to-calculate-the-svg-path-for-an-arc-of-a-circle
    '''
    angleInRadians = angleInDegrees * math.pi / 180.0
    x = centerX + radius * math.cos(angleInRadians)
    y = centerY + radius * math.sin(angleInRadians)
    return x, y

@base.cacofunc
def stats(message, client, *args, **kwargs):
    '''
    **.stats**
    Generates a pie chart, representing the last 1000 messages in this channel. Each wedge represents how many messages were sent by the person as a percentage.
    *Example: `.stats`*
    '''

    #Get the most recent logs
    history = yield from client.logs_from(message.channel, 1000)
    users = { 'totalmsgcount' : 0 }

    #Determine amount of messages sent by each user and total messages.
    #Save message content to be compared later.
    for msg in history:
        if msg.author.name in users:
            users[msg.author.name]['msgcount'] += 1
            users[msg.author.name]['messages'].append(msg)
        else:
            users[msg.author.name] = {}
            users[msg.author.name]['msgcount'] = 1
            users[msg.author.name]['messages'] = []
            users[msg.author.name]['repetitions'] = 0
        users['totalmsgcount'] += 1

    #Variables that store the previous user's SVG vars.
    prevangle = 0
    txtspace = 300
    rxy = [250, 150]

    #Determine amount of times a message has been sent multiple times.
    for usr in users:
        if usr != 'totalmsgcount':

            #Determine what percent of messages are sent by this user
            users[usr]['percentdecimal'] = float(users[usr]['msgcount']) / float(users['totalmsgcount'])
            users[usr]['percent'] = round(users[usr]['percentdecimal'] * 100, 1)

            #Prepare a line to be inserted into an SVG file to create a pie chart.
            users[usr]['angle'] = users[usr]['percentdecimal'] * 360

            usrToPrint = htmlEntities(str(usr).replace('', '').replace('\00',''));
            if len(usr) > 35:
                usrToPrint = str(usr)[:33] + '...'

            x, y = polar2cartesian(150, 150, 100, users[usr]['angle'])
            color = random.choice(colors)

            users[usr]['svgpiestring'] = '<path d="M 150 150 L' + str(rxy[0]) + ' ' + str(rxy[1]) + ' A 100 100 0 0 1 ' + str(x) + ' ' + str(y) + ' z" fill="' + str(color) + '" transform="rotate(' + str(prevangle) + ' 150 150)"/>'

            users[usr]['svgtextstring'] = '<text stroke="black" stroke-width="0.25" fill="' + str(color) + '" x="10" y="' + str(txtspace) + '" font-size="12px" font-family="monospace">' + str(usrToPrint) + ': ' + str(users[usr]['percent']) + '%</text>'
            txtspace += 35
            prevangle += users[usr]['angle']

    #write the SVG file
    result = r'<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg width="300" height="' + str(txtspace) + '" viewBox="0 0 300 ' + str(txtspace) + '" xmlns="http://www.w3.org/2000/svg" version="1.1"><rect width="100%" height="100%" fill="white"/>'

    for usr in users:
        if usr != 'totalmsgcount':
            result += users[usr]['svgpiestring']

    order = list(users)
    random.shuffle(order)

    for usr in order:
        if usr != 'totalmsgcount':
            result += users[usr]['svgtextstring']
    result += r'</svg>'

    with open('tmp.svg', 'w') as data:
        data.write(result)

    subprocess.check_call(['convert', 'tmp.svg', 'tmp.png'])
    yield from client.send_file(message.channel, 'tmp.png')

    '''
    If you want to output directly to the channel as messages, use this:

    for usr in users:
        client.send_message(c, '**{}**: {}% ({} of {})'.format(usr, users[usr]['percent'], users[usr]['msgcount'], users['totalmsgcount']))
    '''
