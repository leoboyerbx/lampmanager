#!/usr/bin/python
import gi
import notify2
import os
import webbrowser
import subprocess
from pathlib import Path

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

_dir_path = os.path.dirname(os.path.realpath(__file__))
_root = Path(_dir_path).parent

class VhostForm(Gtk.Window):

    def __init__(self):

        notify2.init("LAMP Manager", "glib")
        Gtk.Window.__init__(self, title="Add Apache Virtual Host")

        self.vBox = Gtk.Box(spacing=5, orientation=1)
        self.add(self.vBox)

        self.name = ""
        self.path = ""

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
        self.buttonSave.connect("clicked", self.save)
        self.buttonsBox.pack_end(self.buttonSave, False, False, 10)

        self.buttonSave = Gtk.Button(label="Cancel")
        self.buttonSave.connect("clicked", self.cancel)
        self.buttonsBox.pack_end(self.buttonSave, False, False, 0)

    def save(self, widget):
        name = self.nameField.get_text()
        path = self.pathField.get_text()
        if (name == "" or path == ""):
            self.errorMsg('Error', 'Please fill in all the fields to proceed.')
        elif not(os.path.isdir(path)):
            self.errorMsg('Error', '"' + path + '" is not a directory.')
        else:
            self.name = name
            self.path = path

            cmd = "pkexec " + str(_root) + "/bin/addvhost {} {}".format(name, path)
            res = subprocess.call([cmd], shell=True)
            if int(res) == 0:
                n = notify2.Notification("Successfully created Virtual Host",
                                         "You can now access to http://" + name + "/.",
                                         os.path.join(_dir_path, 'img', 'logo.png'))
                n.add_action("open", "Open in browser", self.actions)
                n.show()
                self.destroy()
            else:
                self.errorMsg('Error', "An error occured during virtualhost creation")

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

    def errorMsg(self, message, details):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL, message)
        dialog.format_secondary_text(
            details)
        dialog.run()
        dialog.destroy()

    def cancel(self, widget):
        self.destroy()

    def actions(self, notification, action):
        if action == "open":
            webbrowser.open_new_tab('http://' + self.name + '/')


def add():
    win = VhostForm()
    win.show_all()
