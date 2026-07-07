Name:           mineral
Version:        nightly
Release:        %autorelease
Summary:        A multi-source TUI music player in Rust — ratatui frontend, pluggable channel backends, real streaming playback with lyrics & spectrum.

License:        MIT
URL:            https://github.com/10knamesmore/Mineral
Source0:        https://github.com/10knamesmore/Mineral/archive/refs/heads/main.tar.gz

BuildRequires:  pkgconfig(cargo)
BuildRequires:  pkgconfig(rust)
BuildRequires:  pkgconfig(llvm)
BuildRequires:  pkgconfig(gcc)
BuildRequires:  pkgconfig(alsa-lib)
BuildRequires:  tar
BuildRequires:  git-core

%description
A multi-source TUI music player in Rust — ratatui frontend, pluggable channel backends, real streaming playback with lyrics & spectrum. 

%prep
# GitHub branch archives extract into zmx-main/
%autosetup -n mineral-main

%build
cargo build --release

%install
install -Dm755 target/release/mineral %{buildroot}%{_bindir}/mineral

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/mineral

%changelog
%autochangelog

