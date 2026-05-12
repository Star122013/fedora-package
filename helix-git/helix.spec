%global binary_name hx
%global runtime_directory_path %{_libdir}/helix/runtime

Name:           helix
Version:        nightly
Release:        %{autorelease}
Summary:        A post-modern modal text editor.

License:        MPL-2.0
URL:            https://github.com/helix-editor/helix
Source0:        https://github.com/helix-editor/helix/archive/refs/heads/master.tar.gz

BuildRequires:  rust
BuildRequires:  git
BuildRequires:  clang
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  cargo-rpm-macros


%description
A Kakoune / Neovim inspired editor, written in Rust.

The editing model is very heavily based on Kakoune; during development I found myself agreeing with most of Kakoune's design decisions.


%prep
# GitHub branch archives extract into helix-master/
%autosetup -n helix-master
%cargo_prep


%generate_buildrequires
%cargo_generate_buildrequires


%build
# This will set the default runtime directly in the binary
export HELIX_DEFAULT_RUNTIME=%{runtime_directory_path}
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies


%install
# We can't use %%cargo_install here because it does not support setting --path
install -Dpm 0755 target/release/%{binary_name} %{buildroot}%{_bindir}/%{binary_name}

# Ship the whole runtime tree so Helix has themes, queries, languages.toml,
# tutor, and built grammar shared objects in the expected location.
install -dm 0755 %{buildroot}%{_libdir}/helix
cp -a runtime %{buildroot}%{_libdir}/helix/

# Add shell completions
install -Dpm 0644 contrib/completion/%{binary_name}.bash %{buildroot}/%{bash_completions_dir}/%{binary_name}
install -Dpm 0644 contrib/completion/%{binary_name}.fish %{buildroot}/%{fish_completions_dir}/%{binary_name}.fish
install -Dpm 0644 contrib/completion/%{binary_name}.zsh %{buildroot}/%{zsh_completions_dir}/_%{binary_name}


%files
%license LICENSE LICENSE.dependencies
%doc README.md
%{_bindir}/%{binary_name}
%{runtime_directory_path}
%{bash_completions_dir}/%{binary_name}
%{fish_completions_dir}/%{binary_name}.fish
%{zsh_completions_dir}/_%{binary_name}


%changelog
%autochangelog 
