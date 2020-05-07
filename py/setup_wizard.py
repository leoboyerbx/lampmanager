#!/usr/bin/python
import os
import subprocess
import sys
import gi
from pathlib import Path

gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


_dir_path = os.path.dirname(os.path.realpath(__file__))
_root = Path(_dir_path).parent

# path = sys.argv[1]


class InstallWizard(Gtk.Assistant):
    def __init__(self):
        self.services_list_store = None

        Gtk.Assistant.__init__(self)
        self.connect("cancel", self.done)
        self.connect("close", self.done)
        text_intro = Gtk.Label(
            """Welcome to the LAMP Manager assistant !
This wizard will help you to install LAMP Stack compoments on your computer:
 - Apache
 - PHP
 - Mysql
- phpMyAdmin
- Adminer
- Others...""")

        self.append_page(text_intro)
        self.set_page_type(text_intro, Gtk.AssistantPageType.INTRO)
        self.set_page_title(text_intro, "Introduction")
        self.set_page_complete(text_intro, True)

        self.page2()

    def page2(self):
        page2 = Gtk.Box(spacing=5, orientation=1)

        info = Gtk.Label("Chose which programs to (re)install. If you don't know, leave defaults.")
        page2.pack_start(info, False, False, 10)

        services_list = Gtk.TreeView(self.get_services_store())
        services_list.set_activate_on_single_click(True)
        services_list.set_size_request(500, 200)
        renderer = Gtk.CellRendererText()

        # the column checkbox is created
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)

        column_toggle = Gtk.TreeViewColumn("Install ", renderer_toggle, active=0)
        services_list.append_column(column_toggle)

        cols = ["Name", "Description"]
        for i in range(len(cols)):
            column = Gtk.TreeViewColumn(cols[i], renderer, text=i+1)
            services_list.append_column(column)
        selection = services_list.get_selection()
        selection.set_mode(Gtk.SelectionMode.MULTIPLE)

        page2.pack_start(services_list, True, True, 5)

        self.append_page(page2)
        self.set_page_type(page2, Gtk.AssistantPageType.CONTENT)
        self.set_page_title(page2, "Install Services")

    def done(self, widget):
        Gtk.main_quit()

    def radio_toggle (self, path, path1, path2):
        if path == path1:
            self.services_list_store[path2][0] = False
        if path == path2:
            self.services_list_store[path1][0] = False

    def on_cell_toggled(self, widget, path):
        # Prevent mariadb and mysql interference
        self.radio_toggle(path, '2', '3')
        #Select element
        self.services_list_store[path][0] = not self.services_list_store[path][0]

    def get_services_store(self):
        if self.services_list_store is None:
            self.services_list_store = Gtk.ListStore(bool, str, str)
            programs = [
                [True, "Apache2", "The HTTP server. It allows your computer to host your files and PHP to work. In most cases, you should install Apache2."],
                [True, "PHP", "PHP is an interpreted programming language that generates web content dynamically. Mostly HTML pages"],
                [False, "MySQL", """MySQL is a SQL database server. It's traditionnally installed with PHP. It's maintained by Oracle.
Can't be installed with MariaDB."""],
                [True, "MariaDB", """MariaDB is a Mysql fork, more community-focused, probably more efficient, and 100% MySQL compatible.
It's the default database server on Debian OSes.
Can't be installed with MySQL."""],
                [True, "Adminer", """Adminer is a web-based tool to manage your MySQL/MariaDB database."""],
                [False, "phpMyAdmin", """phpMyAdmin is another web-based tool to manage your MySQL/MariaDB database."""]
            ]
            for row in programs:
                self.services_list_store.append(row)
        return self.services_list_store





def main():
    win = InstallWizard()
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()