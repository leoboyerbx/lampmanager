#!/usr/bin/python
import gi
import notify2
import os
import webbrowser
import subprocess
from pathlib import Path

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from VhostModel import VhostModel

_dir_path = os.path.dirname(os.path.realpath(__file__))
_root = Path(_dir_path).parent


class VhostForm(Gtk.Window):

    def __init__(self, title, name="", path=""):
        Gtk.Window.__init__(self, title=title)
        self.connect("destroy", self.on_destroy)
        self.vhostsModel = VhostModel()

        self.vBox = Gtk.Box(spacing=5, orientation=1)
        self.add(self.vBox)

        self.name = name
        self.path = path

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
        field_box2.pack_start(self.pathField, True, True, 0)
        button_chose_path = Gtk.ToolButton()
        button_chose_path.set_icon_name("folder-open")
        button_chose_path.connect("clicked", self.selectRoot)
        field_box2.pack_start(button_chose_path, True, True, 10)
        self.vBox.pack_start(field_box2, True, True, 0)

        self.buttonsBox = Gtk.Box(spacing=5)
        self.vBox.pack_start(self.buttonsBox, True, True, 10)

        self.buttonSave = Gtk.Button(label="Save")
        self.buttonsBox.pack_end(self.buttonSave, False, False, 10)

        self.buttonCancel = Gtk.Button(label="Cancel")
        self.buttonCancel.connect("clicked", self.cancel)
        self.buttonsBox.pack_end(self.buttonCancel, False, False, 0)


    def selectRoot(self, widget):
        dialog = Gtk.FileChooserDialog("Select Document Root", self,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_filename(self.pathField.get_text())
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.pathField.set_text(dialog.get_filename())

        dialog.destroy()

    def errorMsg(self, message, details):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL, message)
        dialog.format_secondary_text(
            details)
        dialog.run()
        dialog.destroy()


    def on_destroy(self, widget):
        VHostList.update()

    def cancel(self, widget):
        self.destroy()


class VHostFormAdd(VhostForm):

    def __init__(self):
        notify2.init("LAMP Manager", "glib")
        VhostForm.__init__(self, title="Add Apache Virtual Host")

        print(self.buttonSave)
        self.buttonSave.connect("clicked", self.save)

    def save(self, widget):
        name = self.nameField.get_text()
        path = self.pathField.get_text()
        print('hey')
        if (name == "" or path == ""):
            self.errorMsg('Error', 'Please fill in all the fields to proceed.')
        elif not (os.path.isdir(path)):
            self.errorMsg('Error', '"' + path + '" is not a directory.')
        elif self.vhostsModel.exists(name):
            self.errorMsg('Error', '"' + name + '" is already an existing virtualHost.')
        else:
            self.name = name
            self.path = path

            cmd = "pkexec " + str(_root) + "/bin/addvhost {} {}".format(name, path)
            res = subprocess.call([cmd], shell=True)
            if int(res) == 0:
                self.vhostsModel.add(self.name, self.path)
                n = notify2.Notification("Successfully created Virtual Host",
                                         "You can now access to http://" + name + "/.",
                                         os.path.join(_dir_path, 'img', 'logo.png'))
                n.add_action("open", "Open in browser", self.actions)
                n.show()
                self.destroy()
            else:
                self.errorMsg('Error', "An error occured during virtualhost creation")

    def actions(self, notification, action):
        if action == "open":
            webbrowser.open_new_tab('http://' + self.name + '/')


class VHostFormEdit(VhostForm):
    def __init__(self, id, name, path):
        VhostForm.__init__(self, title="Edit Apache Virtual Host", name=name, path=path)
        self.nameField.set_text(name)
        self.nameField.set_sensitive(False)
        self.pathField.set_text(path)
        self.id = id
        self.buttonSave.connect("clicked", self.save)

    def save(self, widget):
        name = self.nameField.get_text()
        path = self.pathField.get_text()
        if (name == "" or path == ""):
            self.errorMsg('Error', 'Please fill in all the fields to proceed.')
        elif not (os.path.isdir(path)):
            self.errorMsg('Error', '"' + path + '" is not a directory.')
        else:
            self.name = name
            self.path = path

            cmd = "pkexec " + str(_root) + "/bin/addvhost {} {}".format(name, path)
            res = subprocess.call([cmd], shell=True)
            if int(res) == 0:
                self.vhostsModel.update(self.id, self.name, self.path)
                self.destroy()
            else:
                self.errorMsg('Error', "An error occured during virtualhost update")


class VHostList(Gtk.Window):
    instances = []

    @classmethod
    def update(cls):
        for instance in cls.instances:
            instance.updateSelf()

    def __init__(self):
        Gtk.Window.__init__(self, title="Apache Virtual Host Management")
        self.vhostsModel = VhostModel()
        VHostList.instances.append(self)
        self.connect("destroy", self.on_destroy)

        self.vBox = Gtk.Box(spacing=5, orientation=1)
        self.add(self.vBox)

        vhost_list_wrapper = Gtk.Box(spacing=5)
        self.vBox.pack_start(vhost_list_wrapper, True, True, 10)

        self.vhost_list = Gtk.TreeView(self.vhostsModel.get_list_store())
        self.vhost_list.set_size_request(500, 200)
        renderer = Gtk.CellRendererText()

        cols = ["#", "Name", "Path"]
        for i in range(len(cols)):
            column = Gtk.TreeViewColumn(cols[i], renderer, text=i)
            self.vhost_list.append_column(column)
        vhost_list_wrapper.pack_start(self.vhost_list, True, True, 10)

        vhost_actions = Gtk.Box(spacing=5, orientation=1)
        add_vhost_btn = Gtk.ToolButton()
        add_vhost_btn.set_icon_name("list-add")
        add_vhost_btn.connect("clicked", self.add_vhost)
        vhost_actions.pack_start(add_vhost_btn, False, False, 0)
        del_vhost_btn = Gtk.ToolButton()
        del_vhost_btn.set_icon_name("list-remove")
        del_vhost_btn.connect("clicked", self.del_vhost)
        vhost_actions.pack_start(del_vhost_btn, False, False, 0)
        edit_vhost_btn = Gtk.ToolButton()
        edit_vhost_btn.set_icon_name("view-more")
        edit_vhost_btn.connect("clicked", self.edit_vhost)
        vhost_actions.pack_start(edit_vhost_btn, False, False, 0)
        open_vhost_btn = Gtk.ToolButton()
        open_vhost_btn.set_icon_name("window-new")
        open_vhost_btn.connect("clicked", self.open_vhost)
        vhost_actions.pack_start(open_vhost_btn, False, False, 0)

        vhost_list_wrapper.pack_start(vhost_actions, False, False, 10)

    def updateSelf(self):
        self.vhost_list.set_model(self.vhostsModel.get_list_store())

    def add_vhost(self, widget):
        subwindow = VHostFormAdd()
        subwindow.show_all()

    def del_vhost(self, widget):
        selection = self.vhost_list.get_selection()
        (model, iter) = selection.get_selected()
        if self.vhostsModel.delete(model[iter][0]):
            VHostList.update()
        else:
            self.errorMsg('Error', "An error occured during virtualhost deletion")

    def edit_vhost(self, widget):
        selection = self.vhost_list.get_selection()
        (model, iter) = selection.get_selected()
        subwindow = VHostFormEdit(model[iter][0], model[iter][1], model[iter][2])
        subwindow.show_all()

    def open_vhost(self, widget):
        selection = self.vhost_list.get_selection()
        (model, iter) = selection.get_selected()
        webbrowser.open_new_tab("http://" + model[iter][1])


    def errorMsg(self, message, details):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL, message)
        dialog.format_secondary_text(details)
        dialog.run()
        dialog.destroy()

    def on_destroy(self, widget):
        VHostList.instances.remove(self)


def add():
    win = VHostFormAdd()
    win.show_all()


def manage():
    win = VHostList()
    win.show_all()
