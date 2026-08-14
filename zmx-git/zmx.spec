%global commit   %(git ls-remote https://github.com/neurosnap/zmx refs/heads/main | head -c8)
%global snap_date %(date -u +%%Y%%m%%d)

Name:           zmx
Version:        0.7.0
Release:        1.%{snap_date}git%{commit}%{?dist}
Summary:        Session persistence for terminal processes.

License:        MIT
URL:            https://github.com/neurosnap/zmx
Source0:        https://github.com/neurosnap/zmx/archive/refs/heads/main.tar.gz

BuildRequires:  (zig >= 0.16 with zig < 0.17)
BuildRequires:  tar
BuildRequires:  git-core

%description
Session persistence for terminal processes.

%prep
# GitHub branch archives extract into zmx-main/
%autosetup -n zmx-main

%build
# Zig does not automatically honor RPM's LDFLAGS for build-id, so pass it explicitly.
# Build for the native target (no -Dtarget) so aarch64 and other arches work.
zig build --build-id=sha1 -Doptimize=ReleaseFast --prefix "zig-out"

%install
install -Dm755 zig-out/bin/zmx %{buildroot}%{_bindir}/zmx
# Generate and install shell completions
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
mkdir -p %{buildroot}%{_datadir}/nushell/completions

zig-out/bin/zmx completions bash > %{buildroot}%{_datadir}/bash-completion/completions/zmx
zig-out/bin/zmx completions zsh  > %{buildroot}%{_datadir}/zsh/site-functions/_zmx
zig-out/bin/zmx completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/zmx.fish
zig-out/bin/zmx completions nu   > %{buildroot}%{_datadir}/nushell/completions/zmx.nu

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/zmx
%{_datadir}/bash-completion/completions/zmx
%{_datadir}/zsh/site-functions/_zmx
%{_datadir}/fish/vendor_completions.d/zmx.fish
%{_datadir}/nushell/completions/zmx.nu

%changelog
%autochangelog

