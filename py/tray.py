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
    def __init__(self, menu, trayText):

        self.ind = appindicator.Indicator.new (
                          "thetool",
                          "",
                          appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-stopped.png'))
        # self.ind.set_attention_icon (os.path.join(_curr_dir, 'img', 'tools-active.png'))
        self.ind.set_menu(menu)
        self.trayText = trayText

    def set_attention(self, attention):
        if attention:
            self.ind.set_status (appindicator.IndicatorStatus.ATTENTION)
        else:
            self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
    def setState(self, state):
        if (state == 2):
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-started.png'))
            self.trayText.set_label('All services Running')
        elif (state == 1):
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'one-started.png'))
            self.trayText.set_label('Some Services Running')
        elif (state == 0): 
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-stopped.png'))
            self.trayText.set_label('All Services Stopped')




def menu():
    menu = gtk.Menu()

    statusItem = gtk.MenuItem("")
    statusItem.set_sensitive(False)
    menu.append(statusItem)

    startAll = gtk.MenuItem("(Re)start All Services")
    startAll.connect('activate', lambda _: lampManager('all', 'restart'))
    menu.append(startAll)

    apacheitem = gtk.ImageMenuItem.new_with_label('Apache2')
    apacheitem.set_image(gtk.Image.new_from_file(os.path.join(_root, '/img/apache.png')))
    apacheitem.set_submenu(serviceMenu('apache', ['start', 'stop', 'restart']))
    apacheitem.set_always_show_image(True)
    menu.append(apacheitem)

    sep = gtk.SeparatorMenuItem()
    menu.append(sep)
    
    exittray = gtk.MenuItem('Exit Tray')
    exittray.connect('activate', quit)
    menu.append(exittray)
    
    menu.show_all()
    return [menu, statusItem]

def serviceMenu(service, actions):
    serviceMenu = gtk.Menu()

    for action in actions:
        command = gtk.MenuItem(action.capitalize())
        command.connect('activate', lambda _: lampManager(service, action))
        serviceMenu.append(command)

    return serviceMenu

def main():
    global tray
    tray = Indicator(*menu())
    lampManager('getstate', '')
    gtk.main()


def lampManager(service, action):
    global tray
    tray.setState(0)
    res = os.popen(str(_root) + "/bin/lampmanager {} {}".format(service, action)).read()
    tray.setState(int(res))
    
def quit(_):
    gtk.main_quit()
if __name__ == "__main__":
    main()