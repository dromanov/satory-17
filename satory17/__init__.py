# -*- coding: utf-8 -*-

import logging

from satory_error import SatoryError

# ────────────────────────────────────────────────────────────────────────────
# Creates independent logger (to untie form CherryPy and other tools).
# ────────────────────────────────────────────────────────────────────────────
def make_my_logger():
    '''Makes console logger on import to start logging.'''
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
    key = (args, frozenset(kw.items()))
    if __TODO.setdefault(key, None) is None:
	say.debug(*args, **kw)
    TODO('add line and file of the emitter from my alchemist sketch')

say.warning('save logs to file')