# -*- coding: utf-8 -*-

from satory17.core         import expose_to_web, PLUG, register_new_PLUG, MAPPER
from satory17.dbase        import DBase
from satory17.satory_error import HtmlStub
from satory17.say          import say, TODO

_html = u"""
<div id='page_toolbar' class='tile_toolbar'>
    <span onclick='satory.update_tile("content-vbox-{self.ID}", "vbox:{self.ID}", "html")'>
        [HTML]
    </span>
    <span onclick='satory.update_tile("content-vbox-{self.ID}", "vbox:{self.ID}", "editor")'>
        [Edit vbox:{self.ID}]
    </span>
</div>
<div id='content-vbox-{self.ID}' class='tile_content'>
{content}
</div>
"""

# TODO: how to do variable length records without serialization.
db = DBase('vbox', key=str, size=int, children=unicode)

class vbox:
    def __init__(self, ID):
        self.ID = ID
        if db.haskey(ID) and ID != '_create_new_':
            self.reload_from_db()
        else:
            self.ID = db.create_new_record_key()
            self.size = 3
            self.children = [None]*3

    def reload_from_db(self):
        assert db.haskey(self.ID), 'no such record in base %s' % self.ID
        item = db.load(self.ID)
        self.size = item['size']
        self.children = eval(item['children'], {})

    @expose_to_web
    def full_page(self):
        return _html.format(self=self, content=self.html())

    @expose_to_web
    def create(self, number, element, child_ID=None):
        if element == 'div_raw':
            new_div_raw = MAPPER['div_raw']('_create_new_')
            new_div_raw.save()
            self.children[int(number)-1] = 'div_raw:' + new_div_raw.ID
            self.save()
        if element == 'child_ID':
            say.warning("VERIFY THIS ID, Man!")
            self.children[int(number)-1] = child_ID
            self.save()
        return """Creating <em>{element}</em>...
        TODO: use redirect or push it trough AJAX.
        """.replace('\n', '<br/>\n').format(ID=self.ID, element=element)

    @expose_to_web
    def html(self):
        res = []
        for number, child in enumerate(self.children, 1):
            if child is None:
                res.append(u"""<h2>Элемент <b>vbox:{self.ID}.{number}</b> отсутствует. Можно создать:<h2>
                    <a href="/_/vbox:{self.ID}/create/{number}/div_raw">Create new div_raw here</a>
                    <a href="/_/vbox:{self.ID}/create/{number}/vbox">Create new vbox</a>
                    <a href="/_/vbox:{self.ID}/create/hbox">Create new hbox</a>
                    Child-ID: <input type="text" id="vbox-{self.ID}-{number}" />
                    <span onclick='window.location="/_/vbox:{self.ID}/create/{number}/child_ID/" + $("vbox-{self.ID}-{number}").val()'>[SUBMIT]</span>
                """.replace('\n', '<br/>\n').format(self=self, number=number))
            else:
                res.append(PLUG(child, 'full_page'))
        return '\n'.join('<div style="border: 1px solid black">%s</div>' % x for x in res)
 
    @expose_to_web
    def editor(self):
        return 'Here will be editor'

    @expose_to_web
    def save(self, size=None, children=None):
        TODO('html5: alert client to update css if required, via web_socket')
        say.warning('implement security checks here')
        TODO('implement security checks here')
        db.save(self.ID, size=size or self.size, 
                children=children or self.children)
        self.reload_from_db()
        return self.html()

register_new_PLUG(vbox, 'vbox')
