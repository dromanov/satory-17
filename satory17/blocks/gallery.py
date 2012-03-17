# -*- coding: utf-8 -*-

import os
import glob
import re

import cherrypy

from satory17.core         import expose_to_web, PLUG, register_new_PLUG
from satory17.dbase        import DBase
from satory17.satory_error import HtmlStub
from satory17.say          import say, TODO

_html = u"""
<div id='toolbar_gallery_{self.ID}' class='tile_toolbar'>
    <span onclick='satory.update_tile("content_gallery_{self.ID}", "gallery:{self.ID}", "html")'>
        [HTML]
    </span>
    <span onclick='satory.update_tile("content_gallery_{self.ID}", "gallery:{self.ID}", "edit")'>
        [Edit gallery:{self.ID}]
    </span>
</div>
<div id='content_gallery_{self.ID}' class='tile_content'>
{gallery_html}
</div>
"""

class gallery:
    def __init__(self, ID):
        self.ID = ID
        self.folder = '/home/henaro/ DAY/satory-17/gallery'
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        assert os.path.isdir(self.folder), 'folder and ROOT is wrong!'
        self.reload()

    def reload(self):
        '''Return a listfile's at the folder'''
        self.list = [f for f in os.listdir(self.folder) 
                     if re.match('\d{4,5}@.*\.(png|jpg|bmp|gif)', f)]

    @expose_to_web
    def full_page(self):
        return _html.format(self=self, gallery_html=self.html())
  
    @expose_to_web
    def html(self):
        exlist = ['<td><img src="/gallery/%s"</td>' % i
                  for i in self.list]
        return u'''
<table width="100%" border="1" cellpadding="10" cellspacing="1">
<tbody>
<tr class="imagerow1">
<td width=1% valign="center" align="center"><input type="button" name="button1" value="&#9668;" onClick="listleft();"></td>
{imgr}
<td width=1% valign="center" align="center"><input type="button" name="button2" value="&#9658;" onClick="listright();"></td>
</tr>
</tbody>
</table>
  '''.format(imgr=''.join(exlist))

    @expose_to_web 
    def edit(self):
        return "<table>%s</table>" % ''.join(
            [('<tr><td><input name="%s_file"></td><td>%s_[x]</td>' +
              '<td><input name="%s.txt_info"></td></tr>') % (i, i[-3:], i[-3:]) 
            for i in self.list]
        )
	
    @expose_to_web	
    def save(self, **kws):
        for i in range(len(kws)):
            try:
                image = kws['%s_image' % i]
                delete = kws['%s_[x]' % i]
                info = kws['%s_info' % i]
                with open (image, 'rb') as f:
                    t = f.read()
                with open (image, 'wb') as f:
                    f.write(t)
            except KeyError:
                break
            self.reload()
            return self.html()
       
register_new_PLUG(gallery, 'gallery')
