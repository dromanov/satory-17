# -*- coding: utf-8 -*-

from satory17.core         import expose_to_web, PLUG, register_new_PLUG
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

        .tile_toolbar span {{
            color: blue;
            text-decoration : underline;
        }}
    </style>
    <style>{self.style}</style>
</head>

<body>
<div id='page_toolbar' class='tile_toolbar'>
    <span onclick='satory.update_tile("page_content", "{self.ID}", "html")'>
        [HTML]
    </span>
    <span onclick='satory.update_tile("page_content", "{self.ID}", "editor")'>
        [Editor]
    </span>
</div>
<div id='page_content' class='tile_content'>
{content}
</div>
<script type="text/javascript" src="js-core.min.js"></script>
<script type="text/javascript" src="js-core.ajax.min.js"></script>
<script>
    // Creates object Satory to represents client side of the engine.
    var satory = (function () {{
        var self = {{}},
            menu_is_visible = false;

        function toggle_menu() {{
            menu_is_visible = !menu_is_visible;
            action = menu_is_visible ? 'show' : 'hide';
            $(document.body).findClass('tile_toolbar').each(action)
        }}

        self.setup_interface = function () {{
            $(document).keydown(function (e) {{
                keycode = e.keyCode ? e.keyCode : e.charCode
                altKey = e.altKey || (keycode == 18)
                ctrlKey = e.ctrlKey || (keycode == 17)
                if (ctrlKey && altKey) {{
                    toggle_menu()
                }}
            }})
        }}

        self.update_tile = function (element, ID, method) {{
            window.status = 'Performing ajax request for ID="' + ID + '"/' + method + ' ...'
            $(element).text('Loading ' + method + '...').load(
                {{"url":"_/" + ID + "/" + method}},
                function () {{
                    window.status = "AJAX Ok";
                }},
                function () {{
                    $(element).text('AJAX error, sorry...')
                }}
            );
        }}

        return self;
    }}());

    $.ready(satory.setup_interface);
</script>"""

db = DBase('html_page', key=int,
           title=unicode, script=unicode, style=unicode, child_ID=str)

class html_page:
    def __init__(self, ID):
        self.ID = ID
        if db.haskey(ID):
            self.reload_from_db()
        else:
            self.title = 'Create new stuff'
            self.script = '/* Here will be collected scripts */'
            self.style = '/* Here will be collected styles */'
            self.child_ID = None

    def reload_from_db(self):
        assert db.hasitem(self.ID), 'bad call to reload'
        item = db.load(ID)
        self.title = item.title
        self.script = item.script
        self.style = item.style
        self.child_ID = item.child_ID

    def full_page(self):
        if self.child_ID is None:
            return _html.format(self=self, content="Here will be constructor")
        return _html.format(self=self, content=PLUG(self.child_ID))

    @expose_to_web
    def html(self):
        return PLUG(self.child_ID)

    @expose_to_web
    def editor(self):
        return _html.format(self=self, content='Here will be editor')

    @expose_to_web
    def save(self, title, script, style, child_ID):
        TODO('html5: alert client to update css if required, via web_socket')
        say.warning('implement security checks here')
        TODO('implement security checks here')
        db.save(title=title, script=script, style=style, child_ID=child_ID)
        self.reload_from_db()
        return self.html()

register_new_PLUG(html_page, 'html_page')
