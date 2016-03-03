Execute the following commands:

1 - Install the following libraries:

    apt-get -y install intltool libdbus-glib-1-dev libgudev-1.0-dev libnl-3-dev libnl-route-3-dev libnl-genl-3-dev uuid-dev libreadline-dev libnss3-dev ppp-dev libndp-dev python-gi python-dbus libnewt-dev

2 - Execute the following commands:

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
    
3 - Copy the network-manager file to /etc/init.d and the NetworkManager.conf to /etc/NetworkManager

    cp network-manager /etc/init.d
    cp NetworkManager.conf /etc/NetworkManager


4 - Enable Network Manager on boot with:

    update-rc.d network-manager defaults

5 - Restart BeagleBone

6 - Check if Network Manager is working running:

    nmtui
