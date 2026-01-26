# Direct-Share
An Android/Linux app to share files quickly and conveniently using Wi-Fi Direct

this project is still in research / experimentation / concept exploration, as I am still:
- exploring how things work.
- testing concepts.
- writing isolated code snippets.
- and don’t yet have a working prototype or even an initial internal build.

## Features:
- as simple as it can get: right click on a file then select "share via Direct-Share"* or open the app, select a file, select the device you want to share with, click share then wait for the other device to accept the connection, and then enjoy your shared file!
- as fast as it can get: no hotspot, no local network, no internet connection required, aka no middleman, just the old and the good and unfortunately forgotten Wi-Fi Direct.

## Acknowledgments:
- the selection of Dear PyGui as the GUI framework was inspired by Zed's HW accelerated GUI.
- [D-Spy](https://gitlab.gnome.org/GNOME/d-spy) for making it easy to inspect D-Bus services.
- thanks to whoever wrote this great [article on D-Bus](https://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html).
- to the devs working on NetworkManager for providing [a code example of how to use Wi-Fi Direct](https://gitlab.freedesktop.org/NetworkManager/NetworkManager/-/blob/main/examples/python/gi/wifi-p2p.py).
- [Bluetooth Devices](https://github.com/Bluetooth-Devices) for making dbus-fast.
