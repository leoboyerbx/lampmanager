#!/usr/bin/python
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class VhostForm(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Add Apache Virtual Host")

        self.vBox = Gtk.Box(spacing=5, orientation=1)
        self.add(self.vBox)

        field_box1 = Gtk.Box(spacing=5)
        name_field_label = Gtk.Label("Virtual host name:")
        field_box1.pack_start(name_field_label, True, True, 10)
        self.nameField = Gtk.Entry()
        self.nameField.set_width_chars(30)
        field_box1.pack_start(self.nameField, True, True, 10)
        self.vBox.pack_start(field_box1, True, True, 10)

        field_box2 = Gtk.Box(spacing=5)
        dir_field_label = Gtk.Label("Document root:")
        field_box2.pack_start(dir_field_label, True, True, 10)
        self.pathField = Gtk.Entry()
        self.pathField.set_width_chars(30)
        field_box2.pack_start(self.pathField, True, True, 0)
        button_chose_path = Gtk.ToolButton()
        button_chose_path.set_icon_name("folder-open")
        button_chose_path.connect("clicked", self.selectRoot)
        field_box2.pack_start(button_chose_path, True, True, 10)
        self.vBox.pack_start(field_box2, True, True, 0)

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


def add():
    win = VhostForm()
    win.show_all()
