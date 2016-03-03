Execute the following commands:

1 - Install the following libraries:

    apt-get -y install intltool libdbus-glib-1-dev libgudev-1.0-dev libnl-3-dev libnl-route-3-dev libnl-genl-3-dev uuid-dev libreadline-dev libnss3-dev ppp-dev libndp-dev python-gi python-dbus libnewt-dev

2 - Uninstall connman with:

    apt-get autoremove connman

3 - Copy NetworManager-1.0.4.tar.xz, NetworkManager.conf and network-manager to BeagleBone

4 - Execute the following commands:

    tar xf NetworkManager-1.0.4.tar.xz
    cd NetworkManager-1.0.4
    ./configure --prefix=/usr\
        --sysconfdir=/etc    \
        --localstatedir=/var \
        --with-nmtui         \
        --disable-ppp        \
        --with-systemdsystemunitdir=no \
        --docdir=/usr/share/doc/network-manager-1.0.4
    make
    make check
    make install
    
5 - Copy the network-manager file to /etc/init.d and the NetworkManager.conf to /etc/NetworkManager

    cp network-manager /etc/init.d
    cp NetworkManager.conf /etc/NetworkManager


6 - Enable Network Manager on boot with:

    update-rc.d network-manager defaults

7 - Restart BeagleBone

8 - Check if Network Manager is working running:

    nmtui