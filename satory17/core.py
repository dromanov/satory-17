# -*- coding: utf-8 -*-

'''
Main entry point: generation of object to handle the request for html content.

Engine takes ID of element in form 'type:id', parses it, creates the element
call to 'type(ID)', and invokes requested method to get content. All extra
arguments are passed to the method.

Simple example is div-block which allows editing of the content inplace using
ajax (see div_raw.py).

Draft example of the usage of this interface:
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
import re

from functools import partial

sys.path.append(os.path.join(os.path.dirname(__file__), "blocks"))

from say          import TODO, say
from satory_error import SatoryError, HtmlStub

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

def PLUG(ID, form='html', *args, **kw):
    '''Returns content of the element 'ID' in given form.'''
    TODO('missing security checks here...')
    ID_components = re.match('^(\w[\w\d_]+):([\d\w_]+)$', str(ID))
    if not ID_components:
	say.error('bad ID: %s', repr(ID))
	return HtmlStub('bad ID')
    block, block_id = ID_components.groups()
    if block not in MAPPER:
	say.error('unknown block: %s' % block)
	return HtmlStub('unknown block')
    tile = MAPPER[block](block_id)
    func = getattr(tile, form, None)
    if func and getattr(func, 'opened_for_web', False):
	return func(*args, **kw)
    else:
	return HtmlStub('call to protected or missing method')

# Modules which use decorators and PLUG method are imported here to avoid
# cross-import conflicts.
from html_page    import html_page
from div_raw      import div_raw
from div_markdown import div_markdown

MAPPER = {
    'html_page'    : html_page,
    'div_raw'      : div_raw,
    'div_markdown' : div_markdown,
}


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
                               |doctest.NORMALIZE_WHITESPACE)
