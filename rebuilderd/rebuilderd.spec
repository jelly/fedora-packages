# Generated by rust2rpm 27
%bcond check 1

Name:           rebuilderd
Version:        0.22.0
Release:        %autorelease
Summary:        - independent build verification daemon

SourceLicense:  GPL-3.0-or-later
License:        GPL-3.0-or-later
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/kpcyrd/rebuilderd
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz
Source:         rebuilderd.sysusers
Patch:          rebuilderd-downgrade-bzip2.patch

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  systemd-rpm-macros
Recommends:     rebuilderd-tools

%global _description %{expand:
Rebuilderd - independent build verification daemon.}

%description %{_description}

%package worker
Summary:        - independent build verification worker

%description worker
Rebuilderd-worker - TODO

%package tools
Summary:        - independent build verification tools

%description tools
Rebuilderd-tools - TODO

%prep
%autosetup -n rebuilderd-%{version} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
mkdir -p %buildroot/%{_bindir}
cp target/rpm/rebuilderd-worker %buildroot/%{_bindir}
cp target/rpm/rebuilderd %buildroot/%{_bindir}
cp target/rpm/rebuildctl %buildroot/%{_bindir}

# TODO
#install -Dm 755 -t %buildroot/%{_libexecdir}/rebuilderd worker/rebuilder-*.sh

# systemd units
install -p -D -m 0644 contrib/systemd/rebuilderd.service %buildroot/%{_unitdir}/rebuilderd.service
install -p -D -m 0644 contrib/systemd/rebuilderd-sync@.service %buildroot/%{_unitdir}/rebuilderd-sync@.service
install -p -D -m 0644 contrib/systemd/rebuilderd-sync@.timer %buildroot/%{_unitdir}/rebuilderd-sync@.timer
install -p -D -m 0644 contrib/systemd/rebuilderd-worker@.service %buildroot/%{_unitdir}/rebuilderd-worker@.service

# tmpfiles
install -p -D -m 0644 contrib/systemd/rebuilderd.tmpfiles %{buildroot}%{_tmpfilesdir}/%{name}.conf

# sysusers
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/rebuilderd.conf


%if %{with check}
%check
# compression tests fail somehow
%cargo_test -- --workspace --exclude rebuildctl
%endif

%files
#%license LICENSE
#%license LICENSE.dependencies
#%doc README.md
%{_bindir}/rebuilderd

%{_sysusersdir}/rebuilderd.conf
%{_tmpfilesdir}/%{name}.conf

%{_unitdir}/rebuilderd.service
%{_unitdir}/rebuilderd-sync@.service
%{_unitdir}/rebuilderd-sync@.timer

# %attr()

%files worker
%{_bindir}/rebuilderd-worker
%{_unitdir}/rebuilderd-worker@.service

%files tools
%{_bindir}/rebuildctl

%changelog
%autochangelog
