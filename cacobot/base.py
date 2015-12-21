# This dictionary will be filled with key-function pairs. The key will be the
# invoker of the function, and the object will be the function to call.
functions = {}

# This decorator is placed on all functions we want to add to CacoBot. It
# automagically makes the function's name the invoker, and adds it to the
# functions dictionary.
def cacofunc(func):
    functions[func.__name__] = func
    return func

# If you're taking the senic tour of the code, you should check out
# cacobot/help.py next.
