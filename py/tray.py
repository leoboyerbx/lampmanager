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
        if (state == 2):
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-started.png'))
        elif (state == 1):
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'one-started.png'))
        elif (state == 0): {
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-stopped.png'))

}



def menu():
    menu = gtk.Menu()

    apacheitem = gtk.ImageMenuItem.new_with_label('Apache2')
    apacheitem.set_image(gtk.Image.new_from_file(os.path.join(_root, '/img/apache.png')))
    apacheitem.set_submenu(apacheMenu())
    apacheitem.set_always_show_image(True)
    menu.append(apacheitem)

    sep = gtk.SeparatorMenuItem()
    menu.append(sep)
    
    exittray = gtk.MenuItem('Exit Tray')
    exittray.connect('activate', quit)
    menu.append(exittray)
    
    menu.show_all()
    return menu

def apacheMenu():
    apacheMenu = gtk.Menu()

    command_apache_start = gtk.ImageMenuItem(gtk.STOCK_OPEN)
    command_apache_start.set_always_show_image(True)
    command_apache_start.connect('activate', apache_start)
    apacheMenu.append(command_apache_start)

    return apacheMenu

def main():
    global tray
    tray = Indicator(menu())
    gtk.main()


def apache_start(_):
    global tray
    tray.setState(0)
    res = os.popen(str(_root) + '/bin/lampmanager apache2 start').read()
    print(res)
    tray.setState(int(res))
    
def quit(_):
    gtk.main_quit()
if __name__ == "__main__":
    main()