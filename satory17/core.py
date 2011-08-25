# -*- coding: utf-8 -*-

'''
Main entry point: generation of object to handle the request for html content.

Engine takes ID of element in form 'type:id', parses it, creates the element
call to 'type(ID)', and invokes requested method to get content. All extra
arguments are passed to the method.

Simple example is div-block which allows editing of the content inplace using
ajax (see div_raw.py).

Draft example of the interface:
    >>> class Block:
    ...	    def __init__(self, ID=None):
    ...		if ID is None:
    ...		    print "Do creation of new instance or Exception here"
    ...		else:
    ...		    print "Load the instance with ID=%s from database" % ID
    ...
    ...	    @expose_to_web
    ...	    @toolbar_icon('image/view.png')
    ...	    def html(self):
    ...		return 'Here will be self.content and link to other stuff'
    ...
    ...	    @expose_to_web
    ...	    @toolbar_icon('image/edit.png')
    ...	    def editor(self):
    ...		return 'Here will be form to edit self.content'
    ...
    ...	    @expose_to_web
    ...	    @toolbar_icon('image/save.png')
    ...	    def save(self, content='Content from form'):
    ...	        print 'Here we save the content to database'
    ...		return self.html()

That is draft scenario to refactor later. Choises are:
class Block:
    # Choise one: attributes in the 'self'
    def __init__(self, ID, icon='...', caption='...'):
	self.icon = icon
	self.caption = caption

    # Choise two: many decorators.
    @expose_to_web
    @toolbar_icon('image/edit.png')
    def editor(self):
	return 'Here will be form to edit self.content'

    # Choise three: complex decorator.
    @expose_to_web(icon='image/edit.png', caption='', links_to={'html' : '..'})
    def editor(self):
	return 'Here will be form to edit self.content'
'''

import sys
import os

from functools import partial

sys.path.append(os.path.join(os.path.dirname(__file__), "blocks"))

from satory17 import TODO, say

# Decorators are before all blocks, so the blocks can import 'satory17.core'.
def expose_to_web(func):
    '''Allows 'PLUG' to call the method of instance.'''
    func.opened_for_web = True
    return func

class toolbar_icon(object):
    '''Decorator with additional arguments (for future development).'''
    def __init__(self, image_URL, caption=None):
	self.image_URL = image_URL
	self.caption = caption

    def __get__(self, obj, objtype=None):
	if obj is None:
	    return self.func
	return partial(self, obj)

    def __call__(self, func):
	def wrapped_func(*args, **kw):
	    return func(*args, **kw)
	# Saves auxiliary information into the function we return to call.
	wrapped_func.image_URL = self.image_URL
	wrapped_func.caption = self.caption
	return wrapped_func

# Note that this modules use decorators above which must stay on top.
from html_paper   import html_paper
from div_raw      import div_raw
from div_markdown import div_markdown

class SatoryError(Exception):
    '''Messages from this exceptions are passed to user.'''
    def __init__(self, value, *args):
	try:
	    self.value = value % args
	except TypeError:
	    log.warning('bad exception formatting: "%s" %% %s' % (value, args))
	    self.value = value

    def __str__(self):
	return str(self.value)


MAPPER = {
    'html_paper'   : html_paper,
    'div_raw'      : div_raw,
    'div_markdown' : div_markdown,
}

def PLUG(ID, form='html', *args, **kw):
    '''Returns content of the element 'ID' in given form.'''
    TODO('security checks here')
    ID_components = re.match('^(\w[\w\d_]+):([\d\w_]+)$', str(ID))
    if not ID_components:
	say.error('bad ID: %s', repr(ID))
	raise SatoryError('bad ID')
    block, block_id = ID_components.groups()
    if block_id not in MAPPER:
	say.error('unknown block: %s' % block)
	raise SatoryError('unknown block')

    tile = MAPPER[block](block_id)
    func = getattr(tile, form, None)
    if func and getattr(func, 'opened_for_web', False):
        return func(*args, **kw)
    else:
        raise SatoryError('call to protected or missing method')


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
                               |doctest.NORMALIZE_WHITESPACE)
