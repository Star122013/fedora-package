# Bibata cursor theme, packaged from the upstream v2.0.7 release.
#
# The upstream build renders SVG -> bitmaps with Node (cbmp + @resvg/resvg-js +
# puppeteer). We skip that entirely and use the prebuilt bitmaps.zip attached to
# the GitHub release, then only run clickgen's `ctgen` to turn the bitmaps into
# XCursor themes (the same approach as the Arch package). clickgen is pure
# Python and is not packaged in Fedora, so it is pip-installed into a throwaway
# venv during %build.

Name:           bibata-cursor-theme
Version:        2.0.7
Release:        1%{?dist}
Summary:        Material based cursor theme (Bibata)

License:        GPL-3.0-or-later
URL:            https://github.com/ful1e5/Bibata_Cursor
Source0:        https://github.com/ful1e5/Bibata_Cursor/archive/refs/tags/v%{version}.tar.gz
# Pre-rendered bitmaps attached to the v%{version} release (sha256
# 87898034589777e77bfa610ed42e6663a6ba57bb91116d296f800199c1bb9183).
Source1:        https://github.com/ful1e5/Bibata_Cursor/releases/download/v%{version}/bitmaps.zip

BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  python3-pip
BuildRequires:  unzip

%description
Bibata is an open source, compact, material designed cursor set with
Modern/Original, Amber/Classic/Ice colour variants in both left- and
right-handed layouts. This package ships the Linux (X11/Wayland) XCursor
themes.

%prep
%autosetup -n Bibata_Cursor-%{version}
# Unpack the pre-rendered bitmaps (bitmaps/<theme>/*.png).
unzip -q %{SOURCE1} -d .

%build
python3 -m venv %{_builddir}/clickgen-venv
. %{_builddir}/clickgen-venv/bin/activate
pip install --no-cache-dir clickgen

declare -A names
names["Bibata-Modern-Amber"]="Yellowish and rounded edge Bibata"
names["Bibata-Modern-Amber-Right"]="Yellowish and rounded edge right-hand Bibata"
names["Bibata-Modern-Classic"]="Black and rounded edge Bibata"
names["Bibata-Modern-Classic-Right"]="Black and rounded edge right-hand Bibata"
names["Bibata-Modern-Ice"]="White and rounded edge Bibata"
names["Bibata-Modern-Ice-Right"]="White and rounded edge right-hand Bibata"
names["Bibata-Original-Amber"]="Yellowish and sharp edge Bibata"
names["Bibata-Original-Amber-Right"]="Yellowish and sharp edge right-hand Bibata"
names["Bibata-Original-Classic"]="Black and sharp edge Bibata"
names["Bibata-Original-Classic-Right"]="Black and sharp edge right-hand Bibata"
names["Bibata-Original-Ice"]="White and sharp edge Bibata"
names["Bibata-Original-Ice-Right"]="White and sharp edge right-hand Bibata"

themes_dir="%{_builddir}/%{buildsubdir}/themes"
for key in "${!names[@]}"; do
  case "$key" in
    *Right*) cfg="configs/right" ;;
    *)       cfg="configs/normal" ;;
  esac
  ctgen "$cfg/x.build.toml" -p x11 \
    -d "bitmaps/$key" \
    -n "$key" \
    -o "$themes_dir" \
    -c "${names[$key]} (v%{version}) XCursors"
done

%install
install -d %{buildroot}%{_datadir}/icons
cp -a %{_builddir}/%{buildsubdir}/themes/Bibata-* %{buildroot}%{_datadir}/icons/

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_datadir}/icons/Bibata-*

%changelog
%autochangelog
