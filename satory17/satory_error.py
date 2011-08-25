# -*- coding: utf-8 -*-

class SatoryError(Exception):
    '''Messages from this exceptions are passed to user.'''
    def __init__(self, value, *args):
	try:
	    self.value = value % args
	except TypeError:
	    say.warning('bad exception formatting: "%s" %% %s' % (value, args))
	    self.value = value

    def __str__(self):
	return str(self.value)
