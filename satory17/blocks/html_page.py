# -*- coding: utf-8 -*-

from satory17.core         import expose_to_web, PLUG
from satory17.dbase        import DBase
from satory17.satory_error import HtmlStub

_html = """<!doctype html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>{self.title}</title>
    <script>{self.script}</script>
    <style>{self.style}</style>
</head>

<body>
{content}
<script type="text/javascript" src="js-core.min.js"></script>
<script>
    // Setup the page when ready.
    $.ready(function () {{
	$(document).keydown(function (e) {{
	    window.status = 'Keypress!'
	    setTimeout("window.status = ''", 500)
	}})
    }});
</script>"""

db = DBase('html_page', key=int,
           title=unicode, script=unicode, style=unicode, child_ID=str)

class html_page:
    def __init__(self, ID):
	self.ID = ID
	if db.haskey(ID):
	    self.reload_from_db()
	else:
	    self.title = 'Dummy title'
	    self.script = '/* Here will be collected scripts */'
	    self.style = '/* Here will be collected styles */'
	    self.child_ID = 'unspecified element'
	    self.body = PLUG(self.child_ID)

    def reload_from_db(self):
	assert db.hasitem(self.ID), 'bad call to reload'
	item = db.load(ID)
	self.title = item.title
	self.script = item.script
	self.style = item.style
	self.child_ID = item.child_ID
	self.body = PLUG(self.child_ID)

    @expose_to_web
    def html(self):
	return _html.format(self=self, content=PLUG(self.child_ID))

    @expose_to_web
    def editor(self):
	return _html.format(self=self, content='Here will be editor')

    @expose_to_web
    def save(self, title, script, style, child_ID):
	say.warning('implement security checks here')
	TODO('implement security checks here')
	db.save(title=title, script=script, style=style, child_ID=child_ID)
	self.reload_from_db()
	return self.html()
