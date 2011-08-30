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
    <style>
	.tile_toolbar {{
	    display : none;
	}}

    </style>
    <style>{self.style}</style>
</head>

<body>
<div id='page_toolbar' class='tile_toolbar'>
Here will be tools to choose display mode of the content.
</div>
<div id='page_content' class='tile_content'>
{content}
</div>
<script type="text/javascript" src="js-core.min.js"></script>
<script>
    // Setup the page when ready.
    satory = {{
	show_menu : function () {{
	    window.status = 'Show menu now'
	    $(document.body).findClass('tile_toolbar').each("show")
	}},
	hide_menu : function () {{
	    window.status = 'Hide menu now'
	    $(document.body).findClass('tile_toolbar').each("hide")
	}}
    }}

    $.ready(function () {{
	$(document).keydown(function (e) {{
	    keycode = e.keyCode ? e.keyCode : e.charCode
	    altKey = e.altKey || (keycode == 18);
	    ctrlKey = e.ctrlKey || (keycode == 17);
	    if (ctrlKey && altKey) {{
		satory.show_menu()
	    }}
	}}).keyup(function (e) {{
	    keycode = e.keyCode ? e.keyCode : e.charCode
	    altKey = e.altKey || (keycode != 18);
	    ctrlKey = e.ctrlKey || (keycode != 17);
	    if (!(satory.ctrlKey && satory.altKey)) {{
		satory.hide_menu()
	    }}
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
