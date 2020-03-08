#!/bin/bash

version_number=$1
output=$2
running_dir=$(pwd)
source_root=$(cd `dirname $0` && pwd)
tmp_dir=$(mktemp -d -t lampbuild-XXXXXXXXXX)

cd $tmp_dir
mkdir DEBIAN
mkdir -p opt/lampmanager
mkdir -p usr/share/applications
mkdir usr/bin

for dir in bin img py lampmanager-tray
do
  cp -r "$source_root/$dir" "./opt/lampmanager/$dir"
done
mkdir opt/lampmanager/data

echo "#!/bin/bash
cd /opt/lampmanager
bash lampmanager-tray
" > usr/bin/lampmanager-tray
chmod +x usr/bin/lampmanager-tray

cp "$source_root/install_scripts/preinst" "$tmp_dir/DEBIAN"
cp "$source_root/install_scripts/postrm" "$tmp_dir/DEBIAN"

chmod 0755 "$tmp_dir/DEBIAN/preinst"
chmod 0755 "$tmp_dir/DEBIAN/postrm"

echo "Package: lampmanager
Version: $version_number
Architecture: all
Depends: python3-notify2, apache2, php, libapache2-mod-php
Maintainer: Léo Boyer
Section: devel
Priority: optional
Installed-Size: 4100
Description: LAMPManager is a GUI Tool to manage your LAMP stack in your development environnement." > ./DEBIAN/control

echo "#!/usr/bin/env xdg-open
[Desktop Entry]
Version=$version_number
Encoding=UTF-8
Name=LAMP Manager
GenericName=LAMPManagerTray
Comment=LAMP Stack managing tool
Exec=lampmanager-tray
Icon=/opt/lampmanager/img/all-started.png
Terminal=false
Type=Application
Categories=Application;Network;Development;
Name[fr_FR]=Gestionnaire de la pile LAMP" > ./usr/share/applications/lampmanager.desktop
chmod +x ./usr/share/applications/lampmanager.desktop

cd $running_dir
dpkg -b $tmp_dir "$running_dir/$output"

rm -rf $tmp_dir