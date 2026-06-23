%global wlroots_abi 20

Name:           swaywm
Version:        1.12
Release:        %{autorelease}
Summary:        i3-compatible Wayland compositor

License:        MIT
URL:            https://swaywm.org/
Source0:        https://github.com/swaywm/sway/releases/download/%{version}/sway-%{version}.tar.gz
Source1:        sway-portals.conf

BuildRequires:  meson >= 1.3
BuildRequires:  pkgconfig(wlroots-0.%{wlroots_abi}) >= 0.%{wlroots_abi}.0
BuildRequires:  pkgconfig(json-c) >= 0.13
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(wayland-server) >= 1.21.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(xkbcommon) >= 1.5.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput) >= 1.26.0
BuildRequires:  pkgconfig(libsystemd) >= 239
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  scdoc >= 1.9.2
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)

Requires:       wlroots%{wlroots_abi}

%description
Sway is a tiling Wayland compositor and a drop-in replacement for the i3
window manager for X11.

%prep
%autosetup -n sway-%{version}

%build
%meson \
  -Dsd-bus-provider=libsystemd \
  -Ddefault-wallpaper=true \
  -Dtray=enabled \
  -Dgdk-pixbuf=enabled \
  -Dman-pages=enabled
%meson_build

%install
%meson_install
install -Dpm 0644 -t %{buildroot}%{_datadir}/xdg-desktop-portal/ %{SOURCE1}

%files
%license LICENSE
%doc README.md
%{_bindir}/sway
%{_bindir}/swaybar
%{_bindir}/swaymsg
%{_bindir}/swaynag
%{_mandir}/man1/sway.1*
%{_mandir}/man1/swaymsg.1*
%{_mandir}/man1/swaynag.1*
%{_mandir}/man5/sway.5*
%{_mandir}/man5/sway-bar.5*
%{_mandir}/man5/sway-input.5*
%{_mandir}/man5/sway-output.5*
%{_mandir}/man5/swaynag.5*
%{_mandir}/man7/sway-ipc.7*
%{_mandir}/man7/swaybar-protocol.7*
%{_datadir}/wayland-sessions/sway.desktop
%{_datadir}/bash-completion/completions/sway
%{_datadir}/bash-completion/completions/swaybar
%{_datadir}/bash-completion/completions/swaymsg
%{_datadir}/fish/vendor_completions.d/sway.fish
%{_datadir}/fish/vendor_completions.d/swaymsg.fish
%{_datadir}/fish/vendor_completions.d/swaynag.fish
%{_datadir}/zsh/site-functions/_sway
%{_datadir}/zsh/site-functions/_swaymsg
%{_datadir}/xdg-desktop-portal/sway-portals.conf
%dir %{_datadir}/backgrounds
%dir %{_datadir}/backgrounds/sway
%{_datadir}/backgrounds/sway/*
%dir %{_sysconfdir}/sway
%dir %{_sysconfdir}/sway/config.d
%config(noreplace) %{_sysconfdir}/sway/config
%config(noreplace) %{_sysconfdir}/sway/config.d/*

%changelog
* Tue Jun 23 2026 cyrene <hyy122013@outlook.com> - 1.12-1
- Initial package for swaywm 1.12
