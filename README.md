# Direct-Share
An Android/Linux app to share files quickly and conveniently using Wi-Fi Direct

this project is still in the pre-alpha (early development) stage so it is still missing many critical features, check issue tracker and milestones for current status.


## what currently works (and what doesn't):
- [ ] connection: 
    - [ ] connecting 2 linux machines
    - [x] connecting a linux machine to an android device (built-in Wi-Fi Direct settings)
    - [ ] connecting an android device to another android device
- [ ] file transfer
    - [ ] android to linux
    - [ ] linux to android

## technical details:
- the selection of Dear PyGui as the GUI framework was inspired by Zed's HW accelerated GUI.
- [D-Spy](https://gitlab.gnome.org/GNOME/d-spy) for making it easy to inspect D-Bus services.
- thanks to whoever wrote this great [article on D-Bus](https://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html).
- to the devs working on NetworkManager for providing [a code example of how to use Wi-Fi Direct](https://gitlab.freedesktop.org/NetworkManager/NetworkManager/-/blob/main/examples/python/gi/wifi-p2p.py).
- [Bluetooth Devices](https://github.com/Bluetooth-Devices) for making dbus-fast.
