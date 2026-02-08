# Direct-Share

Fast local file sharing between **Android and Linux** using **Wi-Fi Direct (P2P)**.

> ⚠️ **Project status: Pre-Alpha**
> This project is under active early development. Many core features are missing or incomplete.
> Expect breakage and unfinished UX.


## Why this exists

File sharing between Android and Linux is still unnecessarily annoying.

Direct-Share aims to be a simple tool that makes local file transfer feel as seamless as:
- Android ↔ Android (Nearby Share / Quick Share)
- Apple AirDrop

…but for **Linux desktops and Android phones**, using **Wi-Fi Direct** (no hotspot required).


## Goals

- **Fast local file transfers** without internet
- **No accounts, no cloud, no pairing nonsense**
- Works across **Linux ↔ Android**
- Simple UI: pick device → pick file → send

## Non-goals
- Bluetooth-based or wifi hotspot transfer
- official support for other operating systems

## Current status (what works / what doesn't)

### Connection
- [x] Linux → Android *(via Android built-in Wi-Fi Direct settings)*
- [ ] Linux ↔ Linux *(not working yet)*
- [ ] Android ↔ Android *(not implemented yet)*

### File transfer
- [ ] Android → Linux
- [ ] Linux → Android

### UX
- [ ] UI/UX is still rough and will change significantly


## Roadmap (planned features)

- Reliable peer discovery
- Proper connection acceptance / rejection flow
- Real file transfer implementation (progress bar, speed, ETA)
- Multi-file support
- Resume/cancel transfers
- Android app (Kotlin / Jetpack Compose)
- Packaging (deb / Flatpak)


## Technical overview

Direct-Share currently relies on Linux Wi-Fi Direct support through:
- **NetworkManager**
- **D-Bus**

The Linux GUI is currently built using **Dear PyGui**.


## Useful tools / references

- [D-Spy](https://gitlab.gnome.org/GNOME/d-spy) — inspect D-Bus services
- Lennart Poettering’s article on D-Bus:
  [The new sd-bus API of systemd](https://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html)
- NetworkManager Wi-Fi Direct example:
  [wifi-p2p.py](https://gitlab.freedesktop.org/NetworkManager/NetworkManager/-/blob/main/examples/python/gi/wifi-p2p.py)
- [dbus-fast](https://github.com/Bluetooth-Devices/dbus-fast)


## Contributing

Contributions are welcome, especially in:
- Wi-Fi Direct connection flow
- D-Bus integration
- Android-side implementation
- UI/UX cleanup

If you're interested, check the issue tracker and milestones.


## License

this project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
