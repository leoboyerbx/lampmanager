#!/usr/bin/python
import os
import gi
from pathlib import Path
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator


_dir_path = os.path.dirname(os.path.realpath(__file__))
_root = Path(_dir_path).parent

class Indicator(object):    
    def __init__(self, menu):

        self.ind = appindicator.Indicator.new (
                          "thetool",
                          "",
                          appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-stopped.png'))
        # self.ind.set_attention_icon (os.path.join(_curr_dir, 'img', 'tools-active.png'))
        self.ind.set_menu(menu)

    def set_attention(self, attention):
        if attention:
            self.ind.set_status (appindicator.IndicatorStatus.ATTENTION)
        else:
            self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
    def setState(self, state):
        switch (state):
            case 2:
                self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-started.png'))
                break
            case 1:
                self.ind.set_icon(os.path.join(_dir_path, 'img', 'one-started.png'))
                break
            case 0:
            default:
                self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-stopped.png'))


def menu():
    menu = gtk.Menu()
    
    command_one = gtk.MenuItem('My Notes')
    command_one.connect('activate', note)
    menu.append(command_one)
    exittray = gtk.MenuItem('Exit Tray')
    exittray.connect('activate', quit)
    menu.append(exittray)
    
    menu.show_all()
    return menu


def main():
    global tray
    tray = Indicator(menu())
    gtk.main()


def note(_):
    print(os.popen(str(_root) + '/bin/lampmanager').read())
    
def quit(_):
    gtk.main_quit()
if __name__ == "__main__":
    main()