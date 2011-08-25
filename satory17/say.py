# -*- coding: UTF-8 -*-

'''
Simple logger created using 'logging' package and separated to untie it from
other tools (e.g. cherrypy which uses and tunes it heavily).
'''

__all__ = ['say']

import logging

def make_console_logger():
    '''Makes console logger on import to start logging.'''
    say = logging.Logger('/')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    f = logging.Formatter('%(name)-5s: %(levelname)-7s %(message)s')
    console.setFormatter(f)
    say.addHandler(console)
    return say

# Now we log to console using our logger.
say = make_console_logger()
