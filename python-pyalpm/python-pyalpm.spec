Name:           python-pyalpm
Version:        0.10.6
Release:        1%{?dist}
Summary:        Python bindings for libalpm

License:        MIT
URL:            https://gitlab.archlinux.org/archlinux/pyalpm
Source0:        %{url}/-/archive/%{version}/pyalpm-%{version}.tar.gz

BuildRequires:  python3-devel python3-pkgconfig python3-setuptools gcc
BuildRequires:  libalpm-devel
Requires:       libalpm

%global _description %{expand:
Python bindings for libalpm
}

%description %_description

%package -n python3-pyalpm
Summary: %{summary}

%description -n python3-pyalpm %_description

%prep
%autosetup -p1 -n pyalpm-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-pyalpm
%license LICENSE
%{python3_sitearch}/*.so
%{python3_sitearch}/pyalpm*egg-info
%{python3_sitearch}/pycman/
%{_bindir}/*

%changelog
* Fri Jun 17 2022 Jelle van der Waa <jelle@archlinux.org> - 0.3.0-1
- Initial version of the package.
