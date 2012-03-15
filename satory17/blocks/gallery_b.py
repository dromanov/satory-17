# -*- coding: utf-8 -*-

from satory17.core         import expose_to_web, PLUG, register_new_PLUG
from satory17.dbase        import DBase
from satory17.satory_error import HtmlStub
from satory17.say          import say, TODO

import os
import glob

_html = u"""
<div id='toolbar_div_{self.ID}' class='tile_toolbar'>
    <span onclick='satory.update_tile("content_div_{self.ID}", "gallery:{self.ID}", "html")'>
        [HTML]
    </span>
    <span onclick='satory.update_tile("content_div_{self.ID}", "gallery:{self.ID}", "editor")'>
        [Edit gallery:{self.ID}]
    </span>
</div>
<div id='content_div_{self.ID}' class='tile_content'>
{self.content}
</div>
"""

#db = DBase('gallery', key=str, content=unicode)

class gallery:
    def __init__(self, ID, imgr):
        self.ID = ID
        self.content = u'''
<table width="100%" border="1" cellpadding="10" cellspacing="1">
<tbody>
<tr class="imagerow1">
<td width=1% valign="center" align="center"><input type="button" name="button1" value="&#9668;" onClick="listleft();"></td>
{imgr}
<td width=1% valign="center" align="center"><input type="button" name="button2" value="&#9658;" onClick="listright();"></td>
</tr>
</tbody>
</table>
 '''.format(imgr=imgr)
        if db.haskey(ID) and ID != '_create_new_':
            self.reload_from_db()
        else:
            self.ID = db.create_new_record_key()

        x = '*/satory-17/img'
        re_names, re_move = [], []

        if os.path.exists(x):
            dir = os.path.abspath(x)

        cont_dir = glob.glob(os.path.join(dir, '*.jpg'))
        names = cont_dir

        for name in cont_dir:
            if '@' in name:
                re_move.append(name)
        for i in range(len(re_move)):
            cont_dir.remove(re_move[i])

        for n in range(len(cont_dir)):
            r = int(6 - len(str(n + 1)))
            pic_n = (r*'0' + str(n+1))
            re_names.append(pic_n + '@' + os.path.split(cont_dir[n])[1])
            re_names[n] = dir +'\\'+ re_names[n]
            os.renames(cont_dir[n], re_names[n])
        with open (re_names[n][:-3]+'txt', 'w+') as f:
            f.write('The screenshot description!')     
#    return re_names, self.content
    
    def reload_from_db(self):
        assert db.haskey(self.ID), 'bad call to reload'
        item = db.load(self.ID)

    @expose_to_web
    def html(self, re_names, start_num=5):
        jb_b, disc, tmp = {}, {}, {}
        for i in range(len(re_names)):
            jp_b[i] = re_names[i]
            f = open(re_names[i][-3:]+'txt', 'r')
            all_lines = f.readlines()
            disc[i] = all_lines
        for i in range(start_num-5, start_num):
            tmp[i] = '<img src="{jb_b[i]}" border="0" width="149" height="134" alt="{disc[i]}" title="Тайтл">'.format(jb_b[i], disc[i])
        for i in range(5):
            imagerow = u'''
  <td width="20%" valign="top">
  <table style="line-height:100%; margin-top:0; margin-bottom:0;" align="center" cellpadding="0" cellspacing="0">
    <tbody>
    <tr>
     <td class="thumbnailTop">
      <p class="thumbnail">
        <img src="{pic_img}" border="0" width="149" height="134" alt="{disc_i}" title="Тайтл">
      </p>
     </td>
    </tr>
    {tmp_i}
    <tr>
     <td class="thumbnailBottom">
      <table class="thumbnail">
        <tbody>
        <tr>
        <td height="25" class="bordercolor2" width="100%">
        <p class="thumbnail"><small>{disc_i}</small></p>
        </td>
        </tr>
    </tbody>
    </table>
    </td>
    </tr>
    </tbody>
  </table>
 </td>'''.format(tmp_i=tmp[i], disc_i=disc[i])
            imgr += imagerow
        return imgr

    @expose_to_web
    def full_page(self):
        return _html.format(self=self)

#    @expose_to_web
#    def editor(self):
#        res = u'''<h3>Enter new content of <em>gallery:{self.ID}</em> here:<br/>
#<textarea rows="15" style="width:80%" 
#          id="content:gallery:{self.ID}" name="content:gallery:{self.ID}">
#{self.content}
#</textarea><br/>
#<span onclick='satory.update_tile("content_div_{self.ID}", 
#                                  "gallery:{self.ID}", "save", 
#                {{"params":{{"content": $("content:gallery:{self.ID}").val()}}, 
#                  "method":"POST"}})'>
#    [Save]
#</span>
#<span onclick='satory.update_tile("content_div_{self.ID}", "gallery:{self.ID}", "html")'>
#    [Cancel]
#</span>
#'''
#        return res.format(self=self)

#    @expose_to_web
#    def save(self, content=None):
#        say.warning('>>> doing saving here: ' + unicode(content))
#        TODO('html5: alert client to update css if required, via web_socket')
#        say.warning('implement security checks here')
#        TODO('implement security checks here')
#        content = self.content if content is None else content
#        db.save(key=self.ID, content=content)
#        self.reload_from_db()
#        return self.html()

register_new_PLUG(gallery, 'gallery')
