Name:           waybar
Version:        0.15.0
Release:        %{autorelease}
Summary:        Highly customizable Wayland bar for Sway and Wlroots based compositors.

License:        MIT
URL:            https://github.com/Alexays/Waybar
Source0:        https://github.com/Alexays/Waybar/archive/refs/tags/%{version}.tar.gz

BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.59.0
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros
 
BuildRequires:  pkgconfig(catch2)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(fmt) >= 8.1.1
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0) >= 0.9.0
BuildRequires:  pkgconfig(gtkmm-3.0)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libgps)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libmpdclient)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(playerctl)
BuildRequires:  pkgconfig(sigc++-2.0)
BuildRequires:  pkgconfig(spdlog) >= 1.10.0
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wireplumber-0.5)
BuildRequires:  pkgconfig(xkbregistry)
BuildRequires:  pkgconfig(libcava)
Requires:       libcava

%description
Highly customizable Wayland bar for Sway and Wlroots based compositors. 

%prep
%autosetup 


%build
%meson \
    -Dcava=enabled  \
    -Dsndio=disabled
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/xdg/%{name}
%config(noreplace) %{_sysconfdir}/xdg/%{name}/config.jsonc
%config(noreplace) %{_sysconfdir}/xdg/%{name}/style.css



%changelog
%autochangelog 
