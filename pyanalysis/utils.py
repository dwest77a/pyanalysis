# encoding: utf-8

__author__ = 'Daniel Westwood'
__date__ = '16 Nov 2022'
__copyright__ = 'Copyright 2022 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'daniel.westwood@stfc.ac.uk'

from pylogger import message, basic

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

if __name__ == "__main__":
    basic(__file__)