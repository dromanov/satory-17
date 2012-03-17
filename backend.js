/*
 * Cookies are used to remember current scrolling position to restore it after
 * reloading page with new LaTeX resolution, updated section and so on.
 */
function createCookie(name, value, days)
{
   expires = "";
   if (days) {
      date = new Date();
      date.setTime(date.getTime() + (days*24*60*60*1000));
      expires = "; expires=" + date.toGMTString();
   }
   document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name)
{
   nameEQ = name + "=";
   ca     = document.cookie.split(';');
   for (i = 0 ; i < ca.length ; ++i) {
      c = ca[i];
      while (c.charAt(0) == ' ')
         c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0)
         return c.substring(nameEQ.length, c.length);
   }
   return null;
}

function eraseCookie(name)
{
   createCookie (name, "", -1);
}

// Updates current element (NOT innerHTML but element itself) using ajax:
//   + id is temporarily changed to avoid name collision;
//   + parent element is replaced by new version on successful load.
function ajax(ID, params, success)
{
   $(ID).text("LOADING...").id(">>>" + ID).load(params, function () {
      $(">>>" + ID).replace($(ID).clone().node)
      if (success)
         success();
   })
}

// Scans form and returns data stored in input fields.
function pack_form(ID)
{
   var fields = {};
   $(ID).children("textarea input text hidden").each(function () {
      fields[$(this).attr("name")] = $(this).val()
   })
   return fields
}

// Creates object 'satory' to wrap a client side of the engine.
var satory = (function () {
   var self = {},
       menu_is_visible = false;

   function toggle_menu() {
      menu_is_visible = !menu_is_visible;
      action = menu_is_visible ? 'show' : 'hide';
      $(document.body).findClass('tile_toolbar').each(action)
   }

   self.setup_interface = function () {
      $(document).keydown(function (e) {
         keycode = e.keyCode ? e.keyCode : e.charCode
         altKey = e.altKey || (keycode == 18)
         ctrlKey = e.ctrlKey || (keycode == 17)
         if (ctrlKey && altKey) {
            toggle_menu()
         }
      })
   }

   // The 'update_tile' calls 'PLUG(ID, method, params)' on server side, and
   // replaces content of dom-element with 'dom_id' by received chunk of html.
   self.update_tile = function (dom_id, ID, method, params) {
      window.status = 'Performing ajax request for ID="' + ID + '"/' + method + ' ...'
      data = {"url":"_/" + ID + "/" + method}
      if (params) {
         // TODO: replace with something like Python's 'dict.update()'...
         for (key in params) {
            data[key] = params[key]
         }
      }
      $(dom_id).text('Loading ' + method + '...').load(
         data,
         function () { window.status = "AJAX Ok"; },
         function () { $(dom_id).text('AJAX error, sorry...'); }
      );
   }
   return self;
}());
