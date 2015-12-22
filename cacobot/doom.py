import cacobot.base as base
import urllib.request

# boris.slipgate.org seems to be misconfigured. I'm sure it'll be fixed
# eventually. Until then, this command is disabled.

# @base.cacofunc # Uncomment to reenable.
def wadidea(message, client, *args, **kwargs):
    """
    **.wadidea**
    *This command was created for the /vr/ Doom server.
    Generates a wad idea from boris.slipgate.org.
    *Example: .wadidea*
    """

    #Download the file.
    result = urllib.request.urlopen("http://boris.slipgate.org/?a=mapgen").read().decode("ISO-8859-1")

    #The webpage will always have this line where the idea begins:
    start = int(result.find('<table align="center" width="400"><tr><td>'))
    start += 42
    #...and this where it ends.
    end = int(result.find('</td></tr></table>\n<hr width="95%">'))

    #Since that's all we're interested in, we make a new var with just that.
    result = result[start:end].strip()

    #Next, we remove all <br>s and line breaks.
    result = result.replace("<br>\n", " ")

    yield from client.send_message(message.channel,  '{}: {}\n\n*Provided by boris.slipgate.org/?a=mapgen*'.format(author.mention, result))
    return
wadidea.server = 'Doom'
