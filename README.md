Introduction
============

CacoBot is a Discord bot designe with a lot of small, useful, and fun commands specializing in memory, recall, and vector image generation. It can be run with a default set of plugins, or integrated and extended in your own code.

**[Please read the terms of service before adding the main CB to your server.](https://github.com/Orangestar12/cacobot/blob/master/tos.md)**

Prerequisites
=============

Install the latest version of [Python](https://www.python.org). CacoBot requires *at minimum* version 3.6, which could cause problems on some Ubuntu based systems.

Install [discord.py](https://github.com/Rapptz/discord.py/). For Python 3.6, you may have to run `pip` as a module. (`python3.6 -m pip install discord.py`)

Download
========

Check out the latest version of CacoBot with `git` (Recommended.)

```
git checkout https://github.com/Orangestar12/cacobot
```

**or**

Download [the latest version of CacoBot](https://github.com/Orangestar12/cacobot/archive/master.zip).

```
wget https://github.com/Orangestar12/cacobot/archive/master.zip
```

Configuration
=============

Create a file called `config.json` with the following structure:

```json
{
    "invokers" : ["."],
    "token" : "Your user token here."
}
```

Activation
==========

You can run CacoBot as a module, which will look for a configuration in the directory `./configs` and activate every command stored in `cacobot/plugins`

```
cd Documents/git/CacoBot
python3.6 -m cacobot
```

You can run `archvile.sh` to do the above, and automatically restart CacoBot every time it closes. (You may need to edit it with your Python binary's name.)

```
cd Documents/git/CacoBot
chmod +x archvile.sh # may not be necessary
./archvile
```

You can import CacoBot like any old package in a Python script, and add only the commands you want or write small, quick commands or something.

```py
import cacobot

from cacobot.plugins import tags

my_cacobot = cacobot.CacoBot('./configs/beta_bot.json')

my_cacobot.run(my_cacobot.config['token'])
```

...or you can inherit and extend the CacoBot class however you want.

```py
import cacobot

class New_CacoBot(cacobot.CacoBot):
```

