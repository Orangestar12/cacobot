import cacobot.base as base
import json, urllib.request, urllib.parse, traceback, re

# The re module already has a find_all, but it works slightly differently from
# the one we've defined here.
def find_all(a_str, sub, start=0, end=0):
    '''Find every instance of a substring.'''
    if end == 0:
        end = len(a_str)
    while True:
        start = a_str.find(sub, start, end)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

@base.cacofunc
async def define(message, client, *args, **kwargs):
    '''
    **{0}define** <*phrase*>
    Scrapes Wiktionary for the dictionary definition of <*phrase*> and formats the first 1-5 results.
    *Example: `{0}define demon`*
    '''
    if message.content.strip()[len(base.config['invoker']):] == 'define':
        await client.send_message(message.channel, '{}: Please provide the word you would like to get the definition from Wiktionary from.'.format(message.author.mention))
    else:
        definition = message.content.split(None, 1)[1].lower() # I'm pretty sure all Wiktionary pages are lowercase.
        encoded = urllib.parse.quote(definition, safe='')

        try:
            # Download the page
            result = urllib.request.urlopen('https://en.wiktionary.org/wiki/{}'.format(encoded)).read().decode('UTF-8')

            # This could be done easier with some XML parsing shit but fuck it
            # I rarely back down from challenges

            # Prelude: Double check the word and save it.
            start = result.find('<title>') + 7
            end = result.find(' - Wiktionary</title>', start)
            title = result[start:end]

            # Step 1: Determine whether the word is primarily a noun or verb.

            # This dictionary will store where each part of speech is.
            speech = {}

            # and this list will store each definition.
            definitions = ['{}: **{}**'.format(message.author.mention, title)]

            # Find the first instance of 'id='Noun''.
            if result.find('id="Noun"') != -1:
                speech['Noun'] = result.find('id="Noun"')

            # Find the first instance of 'id="Verb"'.
            if result.find('id="Verb"') != -1:
                speech['Verb'] = result.find('id="Verb"')

            # Find the first instance of 'id="Adjective"'.
            if result.find('id="Adjective"') != -1:
                speech['Adjective'] = result.find('id="Adjective"')

            # Find the first instance of 'id="Adverb"'.
            if result.find('id="Adverb"') != -1:
                speech['Adverb'] = result.find('id="Adverb"')

            # Find the first instance of 'id="Conjunction"'. (This is just for cheeky fuckers)
            if result.find('id="Conjunction"') != -1:
                speech['Conjunction'] = result.find('id="Conjunction"')

            # There are 2 more parts of speech but they come up so infrequently that
            # I didn't want to check them.

            # Determine which key is smallest
            try:
                lowest = min(speech, key=speech.get) # This will return the part of speech that appears highest on the page.
                definitions.append('*' + str(lowest) + '*')

                # Now that we have the index of the part of speech, we must find the
                # first ordered list after it.
                list_begin = result.find('<ol>', speech[lowest]) + 4
                list_end = result.find('</ol>', list_begin)
                ordered_list = result[list_begin:list_end]

                # Remove any <ul>s in the <ol>. This removes, for example, examples.
                while True:
                    try:
                        ordered_list.index('<ul>')
                    except:
                        break
                    start = ordered_list.find('<ul>')
                    end = ordered_list.find('</ul>') + 6
                    ordered_list = ordered_list[:start] + ordered_list[end:]

                # Now we take each <li> after that and add it to our definitions list
                lists = find_all(ordered_list, '<li>')
                index = 0 # Enumerate won't work in this instance.
                for x in lists:
                    index += 1
                    if index <= 5:
                        y = ordered_list.find('\n', x) # The list items on Wiktionary include lots of things, so we check for newline instead of </li>
                        d = re.sub('<[^<]+?>', '', ordered_list[x:y]) # Strip out html elements.
                        if d != '':
                            definitions.append('  {}: {}'.format(str(index), d))
                        else:
                            index -= 1

                # And finish it off with the link.
                definitions.append('*Read more at https://en.wiktionary.org/wiki/{}*'.format(encoded))

                # Join and send.
                msg = '\n'.join(definitions)
                await client.send_message(message.channel, msg)

            except ValueError: # If no part of speech was found, then just send this:
                await client.send_message(message.channel, message.author.mention + ': I can\'t get the definition of that word, but it exists. Go here: https://en.wiktionary.org/wiki/{}'.format(encoded))
                print(traceback.format_exc())

        except urllib.error.HTTPError: # 404 errors mean the word doesn't exist.
            await client.send_message(message.channel, '{}: That\'s not a word, or Wiktionary doesn\'t have an entry on it.'.format(message.author.mention))
            print(traceback.format_exc())

@base.cacofunc
async def urbdef(message, client, *args, **kwargs):
    '''
    **{0}urbdef** <*phrase*>
    Same as .define, only searches Urban Dictionary instead of Wiktionary.
    *Example: `{0}urbdef doom`*
    '''
    if message.content.strip()[len(base.config['invoker']):] == 'urbdef':
        await client.send_message(message.channel, '{}: Please provide the word you would like to get the definition from Urban Dictionary from.'.format(message.author.mention))
    else:
        definition = message.content.split(None, 1)[1].lower()
        encoded = urllib.parse.quote(definition, safe='')

        try:
            # Urban Dictionary provides a beautiful JSON file in its API. This code is really self-explanatory.
            result = json.loads(urllib.request.urlopen('http://api.urbandictionary.com/v0/define?term={}'.format(encoded)).read().decode('UTF-8'))
            definitions = ['**{}**'.format(result['list'][0]['word'])]
            definitions.append(result['list'][0]['definition'])
            definitions.append('*Read more at {}*'.format(result['list'][0]['permalink']))
            msg = '\n'.join(definitions)
            await client.send_message(message.channel, '{}: {}'.format(message.author.mention,msg))
        except: # I shouldn't be doing a general except, but I forgot what this throws. I think urllib.error.HTTPError?
            await client.send_message(message.channel, '{}: Urban Dictionary doesn\'t have that word.'.format(message.author.mention))
            print(traceback.format_exc())
