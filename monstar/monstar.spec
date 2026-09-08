# Monstar, packaged from the upstream v1.0.1 release tag.
#
# Monstar is a Wayland terminal emulator built on libghostty. Its
# build.zig.zon pins ghostty, zig-wayland, z2d and iterm2-themes as git/URL
# dependencies, all of which Zig fetches over the network at build time (the
# COPR builder has network access, same as the ghostty spec in this repo).
#
# Linking against the vendored libghostty-vt pulls ghostty's source into the
# binary; upstream distributes it under MIT (see LICENSE).

Name:           monstar
Version:        1.0.1
Release:        1%{?dist}
Summary:        A Wayland terminal emulator built on libghostty

License:        MIT
URL:            https://github.com/rockorager/monstar
Source0:        https://github.com/rockorager/monstar/archive/refs/tags/v%{version}.tar.gz

# Zig uses its own bundled clang for translate-c, so no system clang BR is needed.
BuildRequires:  (zig >= 0.16 with zig < 0.17)
BuildRequires:  git-core
BuildRequires:  ncurses
BuildRequires:  ncurses-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pkgconfig(wayland-protocols) >= 1.45
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(xkbcommon)

# D-Bus, systemd and the desktop portals are only spoken to over the session
# bus at runtime and are never linked, so they are runtime deps, not build deps.

%description
Monstar is a fast, feature-rich Wayland terminal emulator built on
libghostty. It supports native Wayland with fractional scaling and IME,
Kitty graphics, OSC 8 hyperlinks, XDG desktop portals, D-Bus notifications,
light/dark theme tracking and bundled color schemes.

%prep
# GitHub tag archives extract into monstar-<version>/
%autosetup -n monstar-%{version}

%build
# Build and install in one step: DESTDIR redirects the install into the
# buildroot, --prefix controls the layout.
export ZIG_GLOBAL_CACHE_DIR=%{_builddir}/zig-cache
mkdir -p "$ZIG_GLOBAL_CACHE_DIR"
DESTDIR=%{buildroot} \
zig build \
  --build-id=sha1 \
  --prefix %{_prefix} \
  -Doptimize=ReleaseFast \
  -Dcpu=baseline \
  -Dstrip=false

%files
%license LICENSE
%doc README.md
%{_bindir}/monstar
%{_datadir}/applications/dev.rockorager.monstar.desktop
%{_datadir}/icons/hicolor/scalable/apps/dev.rockorager.monstar.svg
%{_datadir}/monstar/
%{_mandir}/man1/monstar.1
%{_mandir}/man5/monstar.5

%changelog
%autochangelog
