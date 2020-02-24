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

path = sys.argv[1]


def main():
    page1 = Gtk.Box(spacing=5, orientation=1)

    Gtk.main()


if __name__ == "__main__":
    main()