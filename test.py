#!/usr/bin/env python

# This file is part of Dispatcher
#
# Dispatcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dispatcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dispatcher.  If not, see <http://www.gnu.org/licenses/>.

import sys, os.path, json, time, random
import gi
gi.require_version("WebKit", "3.0")
from gi.repository import WebKit, Gtk, GObject
from jinja2 import Environment, PackageLoader

from sh import fortune


class MainBrace(Gtk.Window):
    def __init__(self, *args, **kargs):
        Gtk.Window.__init__(self, *args, **kargs)
        self.set_default_size(1024, 768)
        self.connect("destroy", Gtk.main_quit)
        self.webview = WebKit.WebView()
        self.add(self.webview)
        self.show_all()
        self.__setup_templates()
        self.load_template("base.html", context={
            'fortunes' : [fortune().strip() for i in range(20)]
        })
        GObject.timeout_add(100, self.test_callback)
        
    def __setup_templates(self):
        """Setup Jinja2 machinery."""

        base_path = os.path.abspath(
            os.path.join(sys.argv[0], "..", "resources"))
        assert os.path.isdir(base_path)
        self.__uri_base = "file://"+base_path+"/"

        self.env = Environment(
            loader=PackageLoader('resources', 'templates'))

    def load_template(self, name, context={}):
        """Load up a Jinja2 template and serve it."""
        template = self.env.get_template(name)
        rendered = template.render(**context)
        self.webview.load_html_string(rendered, self.__uri_base)

    def __call(self, function_name, *args):
        arg_str = json.dumps(args)[1:-1]
        eval_str = "{0}({1})".format(function_name, arg_str)
        self.webview.execute_script(eval_str)
        

    def post_message(self, panel, sender, msg):
        self.__call("post_message", panel, sender, time.time(), msg)


    def test_callback(self, *args, **kargs):
        panel = ["lhs", "rhs"][random.randint(0,1)]
        self.post_message(panel, "nobody", fortune().strip())
        GObject.timeout_add(random.randint(200, 1000), self.test_callback)        
        
        

if __name__ == "__main__":
    w = MainBrace()
    Gtk.main()
