# This dictionary will be filled with key-function pairs. The key will be the
# invoker of the function, and the object will be the function to call.
functions = {}

# This decorator is placed on all functions we want to add to CacoBot. It
# automagically makes the function's name the invoker, and adds it to the
# functions dictionary.
def cacofunc(func):
    functions[func.__name__] = func
    return func

# These next dictionaries and decorators work the same way, but "precommand"
# holds functions that are automatically called *after* successfully
# determining if we have a command, but *before* actually moving on to the
# command, and *postcommand* holds commands that are automatically called *after*
# checking the message.

# Precommands are for things like making sure someone has proper permissions to
# send messages, or logging specific commands to a file or something.

# **WARNINGS**:
# PRECOMMANDS *MUST* RETURN TRUE TO CONTINUE TO THE MESSAGE.
# If you would like a precommand to not continue to the message, return false.
# BOTH PRECOMMANDS AND POSTCOMMANDS MUST USE GENERATORS SOMEWHERE. Else you will
# cause a slew of NoneType error messages.

pres = {}

def precommand(func):
    pres[func.__name__]  = func
    return func

posts = {}

def postcommand(func):
    posts[func.__name__] = func
    return func

# If you're taking the senic tour of the code, you should check out
# cacobot/help.py next.
