# Generated by rust2rpm 27
%bcond check 1
%global debug_package %{nil}

%global crate in-toto

Name:           rust-in-toto
Version:        0.4.0
Release:        %autorelease
Summary:        Library for in-toto

License:        MIT
URL:            https://crates.io/crates/in-toto
Source:         %{crates_source}
Patch:          rust_in-toto-fix-metadata.diff

BuildRequires:  cargo-rpm-macros >= 24
%if %{with check}
BuildRequires:  openssl
%endif

%global _description %{expand:
Library for in-toto.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%doc %{crate_instdir}/GOVERNANCE.md
%doc %{crate_instdir}/MAINTAINERS.txt
%doc %{crate_instdir}/README.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif

%changelog
%autochangelog
