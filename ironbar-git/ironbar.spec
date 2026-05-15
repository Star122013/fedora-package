Name:           ironbar
Version:        nightly
Release:        %autorelease
Summary:        Customisable Wayland GTK4 bar written in Rust.

License:        MIT
URL:            https://github.com/JakeStanger/ironbar
Source0:        https://github.com/JakeStanger/ironbar/archive/refs/heads/master.tar.gz

BuildRequires: rust
BuildRequires: cargo
BuildRequires: gcc-c++
BuildRequires: pkgconfig(gtk4)
BuildRequires: pkgconfig(gtk4-layer-shell-0)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libevdev)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(luajit)
BuildRequires: pkgconfig(libinput)

%description
A customisable and feature-rich GTK4 bar for Wayland compositors, written in Rust.
Ironbar is designed to support anything from a lightweight bar to a full desktop panel with ease.

%prep
%autosetup -n ironbar-master


%build
cargo build --release


%install
install -Dm755 target/release/ironbar %{buildroot}%{_bindir}/ironbar


%files
%license LICENSE
%doc README.md
%{_bindir}/ironbar



%changelog
%autochangelog
