#!/usr/bin/env python

import sys, os.path
import gi
gi.require_version("WebKit", "3.0")
from gi.repository import WebKit
from gi.repository import Gtk
from jinja2 import Environment, PackageLoader


class MainBrace(Gtk.Window):
    def __init__(self, *args, **kargs):
        Gtk.Window.__init__(self, *args, **kargs)
        self.set_default_size(1024, 768)
        self.connect("destroy", Gtk.main_quit)
        self.webview = WebKit.WebView()
        self.add(self.webview)
        self.show_all()
        self.__setup_templates()
        self.load_template("base.html")

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
        

if __name__ == "__main__":
    w = MainBrace()
    Gtk.main()
