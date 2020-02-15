#!/usr/bin/python
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AddForm (Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Add Apache Virtual Host")

        self.vBox = Gtk.Box(spacing=5, orientation=1)
        self.add(self.vBox)

        self.fieldBox1 = Gtk.Box(spacing=5)
        self.vBox.pack_start(self.fieldBox1, True, True, 0)

        nameFieldLabel

        self.buttonsBox = Gtk.Box(spacing=5)
        self.vBox.pack_start(self.buttonsBox, True, True, 0)

        self.buttonSave = Gtk.Button(label="Save")
        self.buttonSave.connect("clicked", self.cancel)
        self.buttonsBox.pack_start(self.buttonSave, True, True, 0)

        self.buttonSave = Gtk.Button(label="Cancel")
        self.buttonSave.connect("clicked", self.cancel)
        self.buttonsBox.pack_start(self.buttonSave, True, True, 0)

    def save(self, widget):
        print("Hello World")
    def cancel(self, widget):
        self.destroy()

def add ():
    win = AddForm()
    win.show_all()
