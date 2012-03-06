# -*- coding: utf-8 -*-

from satory17.core         import expose_to_web, PLUG, register_new_PLUG
from satory17.dbase        import DBase
from satory17.satory_error import HtmlStub
from satory17.say          import say, TODO

_html = """
<div id='toolbar_div_{self.ID}' class='tile_toolbar'>
    <span onclick='satory.update_tile("content_div_{self.ID}", "div_raw:{self.ID}", "html")'>
        [HTML]
    </span>
    <span onclick='satory.update_tile("content_div_{self.ID}", "div_raw:{self.ID}", "editor")'>
        [Edit div_raw:{self.ID}]
    </span>
</div>
<div id='content_div_{self.ID}' class='tile_content'>
{self.content}
</div>
"""

db = DBase('div_raw', key=str, content=unicode)

class div_raw:
    def __init__(self, ID):
        self.ID = ID
        if db.haskey(ID) and ID != '_create_new_':
            self.reload_from_db()
        else:
            self.ID = db.create_new_record_key()
            self.content = 'Create new stuff here\n\n[TODO]Put link to editor here'

    def reload_from_db(self):
        assert db.haskey(self.ID), 'bad call to reload'
        item = db.load(self.ID)
        self.content = item['content']

    @expose_to_web
    def html(self):
        return self.content

    @expose_to_web
    def full_page(self):
        return _html.format(self=self)

    @expose_to_web
    def editor(self):
        res = '''<h3>Enter new content of <em>div_raw:{self.ID}</em> here:<br/>
<textarea rows="15" style="width:80%" id="content:div_raw:{self.ID}">
{self.content}
</textarea>'''
        return res.format(self=self)

    @expose_to_web
    def save(self, content=None):
        TODO('html5: alert client to update css if required, via web_socket')
        say.warning('implement security checks here')
        TODO('implement security checks here')
        content = self.content if content is None else content
        db.save(key=self.ID, content=content)
        self.reload_from_db()
        return self.html()

register_new_PLUG(div_raw, 'div_raw')
