Name:           zmx
Version:        0.5.0
Release:        %autorelease
Summary:        Session persistence for terminal processes.

License:        MIT
URL:            https://github.com/neurosnap/zmx
Source0:        https://github.com/neurosnap/zmx/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  (zig >= 0.15.2 with zig < 0.16)
BuildRequires:  tar
BuildRequires:  git-core
BuildRequires:  glibc-devel

%description
Session persistence for terminal processes.

%prep
%autosetup 

%build
zig build -Doptimize=ReleaseSafe --prefix "zig-out"


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
%{_datadir}/zsh-completion/completions/zmx
%{_datadir}/fish-completion/completions/zmx

%changelog
%autochangelog

