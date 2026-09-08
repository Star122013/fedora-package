# Iosevka 自定义构建: Star/Curly x fontconfig-mono/term/normal, 共 6 个 family。
#
# 一次 `npm run build` 并行产出全部 6 个 plan(共享字形生成, 最快)。
# --jCmd=2 限制并发, 防止 COPR 构建机内存被打爆(每个 job 峰值 >1GB)。

Name:           iosevka-custom-fonts
Version:        34.8.1
Release:        1%{?dist}
Summary:        Custom-built Iosevka (Iosevka Star & Iosevka Curly)

License:        OFL-1.1
URL:            https://github.com/be5invis/Iosevka
Source0:        https://github.com/be5invis/Iosevka/archive/refs/tags/v%{version}.tar.gz
Source1:        private-build-plans.toml

BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  ttfautohint

%description
Custom-built Iosevka typeface generated from private-build-plans.toml.

Two styles shippied, each in three spacing variants (fontconfig-mono / term /
normal), Regular + Bold (with Italic) weights:
    * Iosevka Star     (ss08, Pragmata Pro style, custom zero/g/i)
    * Iosevka Curly    (ss20, Curly style)
All carry C-like ligation set (clike), no cv/ss OpenType features (noCvSs).

%prep
%autosetup -n Iosevka-%{version}
cp %{SOURCE1} private-build-plans.toml

%build
# npm ci 需要可写缓存目录
export npm_config_cache=%{_builddir}/npm-cache
mkdir -p "$npm_config_cache"

npm ci --ignore-scripts
# ttf::<Plan>     只出 TTF, 跳过 webfont(woff2/css), 更快。
#                 verda 的 ttf 目标需要一个 plan 名, 空的 ttf:: 会报
#                 "Build plan for '' not found", 必须逐个列出全部 plan。
# --jCmd=2        限制并行 job, 防 OOM
npm run build -- \
  ttf::IosevkaStar ttf::IosevkaStarTerm ttf::IosevkaStarNormal \
  ttf::IosevkaCurly ttf::IosevkaCurlyTerm ttf::IosevkaCurlyNormal \
  --jCmd=2

%install
install -dm 0755 %{buildroot}%{_datadir}/fonts/%{name}
# Iosevka 把 hinted TTF 放在 dist/<Plan>/TTF/*.ttf (unhinted 在 TTF-Unhinted/),
# 所以必须递归查找, 且只取 TTF/ 目录。用绝对路径, 不依赖 %install 的 cwd。
find %{_builddir}/%{buildsubdir}/dist -path '*/TTF/*.ttf' \
  -exec install -pm 0644 {} %{buildroot}%{_datadir}/fonts/%{name}/ \;

%files
%license LICENSE.md
%{_datadir}/fonts/%{name}/

%changelog
%autochangelog
