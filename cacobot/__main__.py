'''Runs a basic CacoBot with all modules in "plugins"'''

import importlib
import os

import cacobot # import base cacobot necessities

print('Working in ' + os.getcwd())

# add all plugins in plugin folder
for plugin in os.scandir('./cacobot/plugins'):
    if plugin.name.endswith('.py'):
        importlib.import_module('cacobot.plugins.' + plugin.name[:-3])

# build new cacobot and run it
CACOBOT = cacobot.CacoBot('./config/config.json')

CACOBOT.run(CACOBOT.config['token'])
