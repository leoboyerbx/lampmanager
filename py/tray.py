#!/usr/bin/python
import os
import subprocess
import gi
from pathlib import Path
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator


_dir_path = os.path.dirname(os.path.realpath(__file__))
_root = Path(_dir_path).parent

class Indicator(object):    
    def __init__(self, menu, trayText, startAll, stopAll):

        self.ind = appindicator.Indicator.new (
                          "thetool",
                          "",
                          appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-stopped.png'))
        # self.ind.set_attention_icon (os.path.join(_curr_dir, 'img', 'tools-active.png'))
        self.ind.set_menu(menu)
        self.trayText = trayText
        self.startAll = startAll
        self.stopAll = stopAll

    def set_attention(self, attention):
        if attention:
            self.ind.set_status (appindicator.IndicatorStatus.ATTENTION)
        else:
            self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
    def setState(self, state):
        if (state == 2):
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-started.png'))
            self.trayText.set_label('All services Running')
            self.startAll.set_label('Restart All')
            self.stopAll.set_sensitive(True)
        elif (state == 1):
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'one-started.png'))
            self.trayText.set_label('Some Services Running')
            self.startAll.set_label('Restart All')
            self.stopAll.set_sensitive(True)
        elif (state == 0): 
            self.ind.set_icon(os.path.join(_dir_path, 'img', 'all-stopped.png'))
            self.trayText.set_label('All Services Stopped')
            self.startAll.set_label('Start All')
            self.stopAll.set_sensitive(False)




def menu():
    menu = gtk.Menu()

    statusItem = gtk.MenuItem("")
    statusItem.set_sensitive(False)
    menu.append(statusItem)

    sep = gtk.SeparatorMenuItem()
    menu.append(sep)

    startAll = gtk.MenuItem("(Re)start All Services")
    startAll.connect('activate', lambda _: serviceManager('all', 'restart'))
    menu.append(startAll)

    stopAll = gtk.MenuItem("Stop All Services")
    stopAll.connect('activate', lambda _: serviceManager('all', 'stop'))
    menu.append(stopAll)

    sep = gtk.SeparatorMenuItem()
    menu.append(sep)

    apacheitem1 = gtk.ImageMenuItem.new_with_label('Apache2')
    apacheitem1.set_image(gtk.Image.new_from_file(os.path.join(_root, '/img/apache.png')))
    apacheitem1.set_submenu(serviceMenu('apache2'))
    apacheitem1.set_always_show_image(True)
    menu.append(apacheitem1)

    mysqlItem = gtk.ImageMenuItem.new_with_label('MySQL')
    mysqlItem.set_image(gtk.Image.new_from_file(os.path.join(_root, '/img/mysql.png')))
    mysqlItem.set_submenu(serviceMenu('mysql'))
    mysqlItem.set_always_show_image(True)
    menu.append(mysqlItem)

    sep = gtk.SeparatorMenuItem()
    menu.append(sep)

    vhostItem = gtk.MenuItem('Manage Virtual Hosts')
    vhostItem.set_submenu(vhostMenu())
    menu.append(vhostItem)

    sep = gtk.SeparatorMenuItem()
    menu.append(sep)
    
    exittray = gtk.MenuItem('Exit Tray')
    exittray.connect('activate', quit)
    menu.append(exittray)
    
    menu.show_all()
    return [menu, statusItem, startAll, stopAll]

def serviceMenu(service):
    serviceMenu = gtk.Menu()

    command1 = gtk.MenuItem('Start')
    command1.connect('activate', lambda _: serviceManager(service, 'start'))
    serviceMenu.append(command1)

    command2 = gtk.MenuItem('Stop')
    command2.connect('activate', lambda _: serviceManager(service, 'stop'))
    serviceMenu.append(command2)

    command3 = gtk.MenuItem('Restart')
    command3.connect('activate', lambda _: serviceManager(service, 'restart'))
    serviceMenu.append(command3)

    return serviceMenu

def vhostMenu ():
    vhostMenu = gtk.Menu()

    command1 = gtk.MenuItem('Add VirtualHost')
    command1.connect('activate', lambda _: addVhost())
    vhostMenu.append(command1)

    return vhostMenu


def main():
    global tray
    tray = Indicator(*menu())
    serviceManager('getstate', '')
    gtk.main()


def serviceManager(service, action):
    global tray
    tray.setState(0)
    
    cmd = str(_root) + "/bin/servicemanager {} {}".format(service, action)
    res = subprocess.check_output([cmd], shell=True)
    tray.setState(int(res))

def addVhost ():
    print('hey')

def quit(_):
    gtk.main_quit()
if __name__ == "__main__":
    main()