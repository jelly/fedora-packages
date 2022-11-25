Name:           python-flake8-pyproject 
Version:        1.2.1
Release:        1%{?dist}
Summary:        Flake8 plug-in loading the configuration from pyproject.toml

License:        MIT
URL:            https://github.com/john-hen/Flake8-pyproject
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%global _description %{expand:
Flake8 cannot be configured via pyproject.toml, this plug-in registers as a flake8
and loads the configuration from pyproject.toml.
}

%description %_description

%package -n python3-flake8-pyproject
Summary: %{summary}

%description -n python3-flake8-pyproject %_description

%prep
%autosetup -p1 -n Flake8-pyproject-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files flake8p

%check
%pytest

%files -n python3-flake8-pyproject -f %{pyproject_files}
/usr/bin/flake8p

%doc ReadMe.md
%license license.txt

%changelog
* Fri Nov 25 2022 Jelle van der Waa <jelle@vdwaa.nl> - 1.2.1-1
- Initial version of the package.
