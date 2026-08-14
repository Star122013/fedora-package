%global binary_name hx
%global runtime_directory_path %{_libdir}/helix/runtime
%global commit   %(git ls-remote https://github.com/helix-editor/helix refs/heads/master | head -c8)
%global snap_date %(date -u +%%Y%%m%%d)

Name:           helix
Version:        25.07.1
Release:        1.%{snap_date}git%{commit}%{?dist}
Summary:        A post-modern modal text editor.

License:        MPL-2.0
URL:            https://github.com/helix-editor/helix
Source0:        https://github.com/helix-editor/helix/archive/refs/heads/master.tar.gz

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  git
BuildRequires:  clang
BuildRequires:  gcc
BuildRequires:  g++

%description
A Kakoune / Neovim inspired editor, written in Rust.

The editing model is very heavily based on Kakoune; during development I found myself agreeing with most of Kakoune's design decisions.


%prep
# GitHub branch archives extract into helix-master/
%autosetup -n helix-master

%build
# Build like upstream and allow Cargo to fetch dependencies online.
export HELIX_DEFAULT_RUNTIME=%{runtime_directory_path}
export CARGO_HOME=$PWD/.cargo
mkdir -p "$CARGO_HOME"
cargo build --profile opt --locked 


%install
install -Dpm 0755 target/opt/%{binary_name} %{buildroot}%{_bindir}/%{binary_name}

# Ship the runtime tree, but drop bundled grammar source/build directories.
# They contain temporary ELF/node artifacts (for example a.out) that are not
# meant to be packaged and make find-debuginfo fail on missing build-ids.
install -dm 0755 %{buildroot}%{_libdir}/helix
cp -a runtime %{buildroot}%{_libdir}/helix/
rm -rf %{buildroot}%{runtime_directory_path}/grammars/sources

# Add shell completions
install -Dpm 0644 contrib/completion/%{binary_name}.bash %{buildroot}/%{bash_completions_dir}/%{binary_name}
install -Dpm 0644 contrib/completion/%{binary_name}.fish %{buildroot}/%{fish_completions_dir}/%{binary_name}.fish
install -Dpm 0644 contrib/completion/%{binary_name}.zsh %{buildroot}/%{zsh_completions_dir}/_%{binary_name}


%files
%license LICENSE
%doc README.md
%{_bindir}/%{binary_name}
%{runtime_directory_path}
%{bash_completions_dir}/%{binary_name}
%{fish_completions_dir}/%{binary_name}.fish
%{zsh_completions_dir}/_%{binary_name}


%changelog
%autochangelog 
