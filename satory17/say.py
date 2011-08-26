# -*- coding: utf-8 -*-

import logging

# ────────────────────────────────────────────────────────────────────────────
# Creates independent logger (to untie form CherryPy and other tools).
# ────────────────────────────────────────────────────────────────────────────
def make_my_logger():
    say = logging.Logger('/')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    f = logging.Formatter('%(name)-5s: %(levelname)-7s %(message)s')
    console.setFormatter(f)
    say.addHandler(console)
    return say

# Now we log to console using our logger.
say = make_my_logger()


__TODO = {}
def TODO(*args, **kw):
    '''Saves message only once as a reminder.'''
    key = (args, frozenset(kw.items()))
    if __TODO.setdefault(key, None) is None:
	say.debug(*args, **kw)

TODO('add line and file of the emitter from my alchemist sketch is TODO')
TODO('save logs to file')
say.warning('save logs to file')
