Name:           zmx
Version:        nightly
Release:        %autorelease
Summary:        Session persistence for terminal processes.

License:        MIT
URL:            https://github.com/neurosnap/zmx
Source0:        https://github.com/neurosnap/zmx/archive/refs/heads/main.tar.gz

BuildRequires:  (zig >= 0.15.2 with zig < 0.16)
BuildRequires:  tar
BuildRequires:  git-core

%description
Session persistence for terminal processes.

%prep
# GitHub branch archives extract into zmx-main/
%autosetup -n zmx-main

%build
# Zig does not automatically honor RPM's LDFLAGS for build-id, so pass it explicitly.
# Avoid pinning an exact glibc minor version; Zig 0.15 currently falls back from 2.43 to 2.42.
zig build --prefix "zig-out"

%install
install -Dm755 zig-out/bin/zmx %{buildroot}%{_bindir}/zmx
# Generate and install shell completions
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d

zig-out/bin/zmx completions bash > %{buildroot}%{_datadir}/bash-completion/completions/zmx
zig-out/bin/zmx completions zsh  > %{buildroot}%{_datadir}/zsh/site-functions/_zmx
zig-out/bin/zmx completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/zmx.fish

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/zmx
%{_datadir}/bash-completion/completions/zmx
%{_datadir}/zsh/site-functions/_zmx
%{_datadir}/fish/vendor_completions.d/zmx.fish

%changelog
%autochangelog

