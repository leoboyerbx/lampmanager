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
This wizard will help you to install LAMP Stack compoments on your computer: Apache, PHP, Mysql, PHPMyadmin, Adminer...""")

        self.append_page(text_intro)
        self.set_page_type(text_intro, Gtk.AssistantPageType.INTRO)
        self.set_page_title(text_intro, "Introduction")

    def page2(self):
        page2 = Gtk.Box(spacing=5, orientation=1)

        info = Gtk.Label("The following programs are NOT installed. Select the ones you want to install:")
        page2.pack_start(info, False, False, 10)

        services_list = Gtk.TreeView(self.get_services_store())
        services_list.set_size_request(500, 200)
        renderer = Gtk.CellRendererText()

        cols = ["Name", "Description"]
        for i in range(len(cols)):
            column = Gtk.TreeViewColumn(cols[i], renderer, text=i)
            services_list.append_column(column)
        page2.pack_start(services_list, True, True, 10)

        self.append_page(page2)
        self.set_page_type(page2, Gtk.AssistantPageType.CONTENT)

    def done(self, widget):
        Gtk.main_quit()

    def get_services_store(self):
        if self.services_list_store is None:
            self.services_list_store = Gtk.ListStore(str, str)
            programs = [
                ["Apache2", "description"], ["MySQL", "description"], ["PHP", "description"]
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