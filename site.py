#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
That is http/cherrypy frontend to the Satory-17.

CherryPy converts incoming http requests into calls to the engine.
"""

from __future__ import with_statement

import sys
import os
import cgi
import traceback

import cherrypy

import satory17

from satory17.core import PLUG
from satory17 import html_page, div_raw

class FrontPage:
    @cherrypy.expose
    @cherrypy.tools.encode()
    def default(self, paper="frontpage", *args, **KWs):
        """Frontend: shows entire paper or redirects to a special page."""
        cherrypy.response.headers['Content-Type'] = "text/html"
        wrapper = satory17.html_page(ID=unicode(paper))
        return wrapper.full_page()

    @cherrypy.expose
    @cherrypy.tools.encode()
    def debug(self, ID=None, *args, **KWs):
        """Debug environment."""
        cherrypy.response.headers['Content-Type'] = "text/html"
        return u"Debugging '%s'<hr/>Args: %s<hr/>KWs: %s" % (ID, args, KWs)

    @cherrypy.expose
    @cherrypy.tools.encode()
    def _(self, ID, method="html", *args, **kws):
        """AJAX backend: forwards requests to handlers."""
        cherrypy.response.headers['Content-Type'] = "text/html"
        try:
            res = PLUG(ID, method, *args, **kws)
        except:
            # Reporting an exeption inside of ajax call.
            esc = cgi.escape
            args = ["%s : %s" % (esc(k), esc(kws[k])) for k in kws]
            res = """ <h2>AJAX error:</h2>
                      %s<hr />
                      <pre>%s</pre>
            """ % ("<br>".join(args), traceback.format_exc())
        return res

# Contacts cherrypy's config file.
root_dir = os.path.dirname(__file__)
cfg_file = os.path.join(root_dir, 'site.conf')
cherrypy.tree.mount(FrontPage(), config=cfg_file)

if __name__ == '__main__':
    cherrypy.quickstart(config=os.path.join(root_dir, 'site.conf'))
