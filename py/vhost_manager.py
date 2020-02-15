#!/usr/bin/python
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AddForm (Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Add Apache Virtual Host")
        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.cancel)
        self.add(self.button)

    def save(self, widget):
        print("Hello World")
    def cancel(self, widget):
        self.destroy()

def add ():
    win = AddForm()
    win.show_all()
