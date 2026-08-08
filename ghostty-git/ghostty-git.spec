# Ghostty nightly build tracking the upstream main branch.
#
# The COPR builder has network access, so we let Zig fetch all of Ghostty's
# dependencies (build.zig.zon) at build time rather than vendoring them.

Name:           ghostty-git
Version:        nightly
Release:        %autorelease
Summary:        A fast, feature-rich terminal emulator written in Zig (main branch)

License:        MIT AND MPL-2.0 AND OFL-1.1 AND CC0-1.0 AND Apache-2.0
URL:            https://ghostty.org/
Source0:        https://github.com/ghostty-org/ghostty/archive/refs/heads/main.tar.gz

BuildRequires:  zig
BuildRequires:  git-core
BuildRequires:  gcc
BuildRequires:  pandoc-cli
BuildRequires:  blueprint-compiler
BuildRequires:  ncurses
BuildRequires:  ncurses-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libX11-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(zlib)

# Suppress -fno-semantic-interposition warning noise from rpmbuild
%global _disable_debuginfo_attributes 1

Conflicts:       ghostty

%description
Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses
platform-native UI and GPU acceleration. This is a nightly build tracking the
upstream main branch.

%prep
%autosetup -n ghostty-main

%build
export ZIG_GLOBAL_CACHE_DIR=%{_builddir}/zig-cache
mkdir -p "$ZIG_GLOBAL_CACHE_DIR"
zig build \
  -Doptimize=ReleaseFast \
  -Dtarget=x86_64-linux-gnu \
  -Dcpu=baseline \
  -Dpie=true \
  -Demit-docs \
  -Demit-terminfo \
  -Demit-termcap

%install
export ZIG_GLOBAL_CACHE_DIR=%{_builddir}/zig-cache
DESTDIR=%{buildroot} \
zig build install \
  --release=fast \
  -Dcpu=baseline \
  -Dpie=true \
  -Demit-docs \
  -Demit-terminfo \
  -Demit-termcap \
  --prefix %{_prefix} \
  --prefix-lib-dir %{_libdir} \
  --prefix-exe-dir %{_bindir} \
  --prefix-include-dir %{_includedir}

# Ghostty installs its systemd user unit to share/ when not in
# "system package mode"; systemd only searches lib/, so move it.
mkdir -p %{buildroot}%{_libdir}/systemd/user
mv %{buildroot}%{_datadir}/systemd/user/app-com.mitchellh.ghostty.service \
   %{buildroot}%{_libdir}/systemd/user/
rmdir %{buildroot}%{_datadir}/systemd/user 2>/dev/null || true

# Don't clash with the ncurses-term ghostty entry on F42+
%if 0%{?fedora} >= 42
rm -rf %{buildroot}%{_datadir}/terminfo/g/ghostty
%endif

%files
%license LICENSE
%doc README.md
%{_bindir}/ghostty
%{_libdir}/systemd/user/app-com.mitchellh.ghostty.service
%{_datadir}/ghostty/
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/dbus-1/services/com.mitchellh.ghostty.service
%{_datadir}/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_datadir}/nautilus-python/extensions/ghostty.py
%{_datadir}/nvim/site/compiler/ghostty.vim
%{_datadir}/nvim/site/ftdetect/ghostty.vim
%{_datadir}/nvim/site/ftplugin/ghostty.vim
%{_datadir}/nvim/site/syntax/ghostty.vim
%{_datadir}/vim/vimfiles/compiler/ghostty.vim
%{_datadir}/vim/vimfiles/ftdetect/ghostty.vim
%{_datadir}/vim/vimfiles/ftplugin/ghostty.vim
%{_datadir}/vim/vimfiles/syntax/ghostty.vim
%{_iconsdir}/hicolor/16x16/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/32x32/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/128x128/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/256x256/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/512x512/apps/com.mitchellh.ghostty.png
%{_iconsdir}/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
%{_mandir}/man1/ghostty.1.gz
%{_mandir}/man5/ghostty.5.gz
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/zsh/site-functions/_ghostty
%{bash_completions_dir}/ghostty.bash
%if 0%{?fedora} < 42
%{_datadir}/terminfo/g/ghostty
%endif
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/terminfo/ghostty.terminfo
%{_datadir}/terminfo/ghostty.termcap

%changelog
%autochangelog
