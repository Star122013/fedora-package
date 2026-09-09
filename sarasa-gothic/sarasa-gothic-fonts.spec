# Sarasa Gothic, packaged from the upstream pre-built TTC release.
#
# The project is a huge CJK composite font (Inter + Iosevka + Source Han Sans):
# 5 spacing styles (Gothic / UI / Mono / Term / Fixed, plus Slab variants) x
# 6 orthographies x 10 weights x italic. Building it from source needs Node,
# AFDKO, ttfautohint and ~16 GiB of RAM just to bundle the TTCs, so we ship the
# upstream hinted TrueType Collections instead.
#
# The TTC archive packs every family into 10 collection files and a TTC cannot
# be split, hence the single all-in-one package. Per-family TTF archives exist
# upstream but balloon to ~1.5 GiB per family, so TTC is the only sane choice.

Name:           sarasa-gothic-fonts
Version:        1.0.41
Release:        1%{?dist}
Summary:        A CJK composite font based on Inter, Iosevka and Source Han Sans

License:        OFL-1.1
URL:            https://github.com/be5invis/Sarasa-Gothic
Source0:        https://github.com/be5invis/Sarasa-Gothic/releases/download/v%{version}/Sarasa-TTC-%{version}.7z
Source1:        https://raw.githubusercontent.com/be5invis/Sarasa-Gothic/v%{version}/LICENSE

# Fonts are architecture independent; noarch also disables debuginfo/debugsource
# generation (an empty debugsourcefiles.list would otherwise fail the build).
BuildArch:      noarch
BuildRequires:  7zip

%description
Sarasa Gothic is a CJK composite font built from Inter, Iosevka and Source Han
Sans. It provides the Gothic, UI, Mono, Term and Fixed spacing styles (plus
their Slab variants) in ten weights with matching italics, covering the CL, HC,
J, K, SC and TC orthographies.

This package installs the hinted TrueType Collections (TTC) from the upstream
release.

%prep
# The release artifact is a flat 7z of Sarasa-*.ttc, not a tarball, so there is
# no autosetup here.
mkdir -p ttc
7z x -y -o./ttc %{SOURCE0} >/dev/null
cp %{SOURCE1} LICENSE

%install
install -dm 0755 %{buildroot}%{_datadir}/fonts/%{name}
install -pm 0644 ttc/*.ttc %{buildroot}%{_datadir}/fonts/%{name}/

%files
%license LICENSE
%{_datadir}/fonts/%{name}/

%changelog
%autochangelog
