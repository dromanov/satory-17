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
'''

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "blocks"))

# Decorators are here to be included in all 'html_paper.py', etc.
def expose_to_web(func):
    '''Allows 'PLUG' to call the method of instance.'''
    func.opened_for_web = True
    return func

def toolbar_icon(image_URL, caption=None):
    def wrap(func):
	print "Here will be something..."
	new_func = lambda : None
	update_wrapper(new_func, func)
	return new_func
    return wrap


from html_paper   import html_paper
from div_raw      import div_raw
from div_markdown import div_markdown

mapper = {
    'html_paper'   : html_paper,
    'div_raw'      : div_raw,
    'div_markdown' : div_markdown,
}


def PLUG(ID, method='html', *args, **KWs):
    return ''

if __name__ == '__main__':
    #import sys
    #reload(sys)
    #sys.setdefaultencoding("utf-8")

    #import doctest
    #doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
                               #|doctest.NORMALIZE_WHITESPACE)

    from functools import partial

    class decorator(object):
	def __init__(self, arg1):
	    print 'd.__init__>>>', arg1
	    self.arg1 = arg1

	def __get__(self, obj, objtype=None):
	    if obj is None:
		return self.func
	    return partial(self, obj)

	def __call__(self, func):
	    print "c.__call__>>>", func, self.arg1
	    def wrapped_func(*args, **kw):
		print "Inside wrapped_f()", args, kw
		return func(*args, **kw)
	    return wrapped_func

    # example usage
    class Test(object):
        v = 0
        @decorator('argument1')
        def inc_add(self, arg):
	    print self, arg
            self.v += 1
            return self.v + arg

    t1 = Test()
    t2 = Test()

    print t1.inc_add(2)
    print t1.inc_add(2)
    print t2.inc_add(2)

#    doctest.testfile('core.test',
#		     encoding='utf-8')
