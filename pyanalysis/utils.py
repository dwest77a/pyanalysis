# encoding: utf-8

__author__    = 'Daniel Westwood'
__date__      = '16 Nov 2022'
__copyright__ = 'Copyright 2022 United Kingdom Research and Innovation'
__license__   = 'BSD - see LICENSE file in top-level package directory'
__contact__   = 'daniel.westwood@stfc.ac.uk'

from pylogger import message, basic

# Useful functions to have in data analysis/visualisation

def buffer(item, length):
    """
    Simple String Formatting Function
     - Returns a string with added whitespace or removed chars
       such that new string is a specific length.
    """
    buff = ''
    if len(item) >= length:
        item = item[:length]
    else:
        for x in range(0,length-len(item)):
            buff += ' '
    return str(item+buff)

def accept_input(prompt, accepted='', atype='', fileroot=''):
    if type(accepted) != list:
        accepted = [accepted]
    valid_entry = False
    while not valid_entry:
        user_in = input(prompt)
        if accepted == [''] or user_in in accepted:
            if atype == 'int':
                try:
                    user_in = int(user_in)
                    valid_entry = True
                except:
                    print('Error: Input does not meet "int" type requirements, please enter a number')
            elif atype == 'file':
                if os.path.isfile(fileroot+user_in):
                    valid_entry = True
                else:
                    print('Error: Requested file not found')
            else:
                valid_entry = True
        else: 
            print('Error: Input not in accepted form')
    return user_in

if __name__ == "__main__":
    basic(__file__)