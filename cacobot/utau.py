import discord
import cacobot.base as base

@base.cacofunc
def limbo(message, client):
    '''
    **.limbo** [*mention*]
    *This command was created for the Vocaloid server. Just for Rodea. ;)*
    This is a shortcut to add the "Limbo" role to a user. If your server has no "Limbo" role, this will fail.
    *Example: `.limbo @CacoBot`*
    '''
    if message.channel.permissions_for(message.author).ban_members:
        try:
            foreboden = discord.utils.find(lambda m: m.name == 'Limbo', message.server.roles)
            if foreboden != None:
                for ment in message.mentions:
                    yield from client.replace_roles(ment, foreboden)
                    yield from client.send_message(message.channel, '{}: {} has been Limbo\'d.'.format(message.author.mention, ment.name))
            else:
                yield from client.send_message(message.channel, '{}: You must create a role named \'Limbo\' before you can use this command.'.format(message.author.mention))
        except discord.Forbidden:
            yield from client.send_message(message.channel, '{}: I do not have the permission to perform this command yet.'.format(message.author.mention))
    else:
        yield from client.send_message(message.channel, '{}: You do not have the permission to manage roles.'.format(message.author.mention))
limbo.server = 'Vocaloid'
