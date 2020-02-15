#!/usr/bin/python
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AddForm (Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Add Apache Virtual Host")

        self.vBox = Gtk.Box(spacing=5, orientation=1)
        self.add(self.vBox)

        fieldBox1 = Gtk.Box(spacing=5)
        nameFieldLabel = Gtk.Label("Virtual host name:")
        fieldBox1.pack_start(nameFieldLabel, True, True, 10)
        self.nameField = Gtk.Entry()
        self.nameField.set_width_chars(30)
        fieldBox1.pack_start(self.nameField, True, True, 10)
        self.vBox.pack_start(fieldBox1, True, True, 10)

        fieldBox2 = Gtk.Box(spacing=5)
        dirFieldLabel = Gtk.Label("Document root:")
        fieldBox2.pack_start(dirFieldLabel, True, True, 10)
        self.pathField = Gtk.Entry()
        self.pathField.set_width_chars(30)
        fieldBox2.pack_start(self.pathField, True, True, 0)
        buttonChosePath = Gtk.ToolButton()
        buttonChosePath.set_icon_name("folder-open")
        buttonChosePath.connect("clicked", self.selectRoot)
        fieldBox2.pack_start(buttonChosePath, True, True, 10)
        self.vBox.pack_start(fieldBox2, True, True, 0)

        self.buttonsBox = Gtk.Box(spacing=5)
        self.vBox.pack_start(self.buttonsBox, True, True, 10)

        self.buttonSave = Gtk.Button(label="Save")
        self.buttonSave.connect("clicked", self.cancel)
        self.buttonsBox.pack_end(self.buttonSave, False, False, 10)

        self.buttonSave = Gtk.Button(label="Cancel")
        self.buttonSave.connect("clicked", self.cancel)
        self.buttonsBox.pack_end(self.buttonSave, False, False, 0)

    def save(self, widget):
        print("Hello World")

    def selectRoot(self, widget):
        dialog = Gtk.FileChooserDialog("Select Document Root", self,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.pathField.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def cancel(self, widget):
        self.destroy()

def add ():
    win = AddForm()
    win.show_all()
