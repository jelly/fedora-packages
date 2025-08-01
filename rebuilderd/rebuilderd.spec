# Generated by rust2rpm 27
%bcond check 1

Name:           rebuilderd
Version:        0.24.0
Release:        %autorelease
Summary:        Independent build verification daemon

SourceLicense:  GPL-3.0-or-later
License:        GPL-3.0-or-later
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/kpcyrd/rebuilderd
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz
Source:         rebuilderd.sysusers
Patch:          0001-worker-implement-custom-fedora-comparison.patch
Patch:          0001-tools-filter-other-architectures-in-a-repository.patch
Patch:          0001-Downgrade-serde-xml-rs-nix-for-Fedora-packaging.patch

Requires:       shared-mime-info
BuildRequires:  shared-mime-info
BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  systemd-rpm-macros
BuildRequires:  scdoc
Recommends:     rebuilderd-tools


%description
Independent build verification daemon.

Rebuilderd monitors and reproduces binary packages from source.

%package worker
Summary: Independent build verification worker

%description worker
This package contains the rebuilderd-worker service.

The worker connects to rebuilderd for a new build task, automatically rebuilds
and publishes the results to rebuilderd.

%package tools
Summary: Independent build verification tools

%description tools
This package contains rebuildctl, a CLI tool which queries rebuilderd and can
show the worker, queue and package status.

%prep
%autosetup -n rebuilderd-%{version} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
make docs

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

# config files
install -p -D -m 0600 contrib/confs/rebuilderd-worker.conf %{buildroot}%{_sysconfdir}/rebuilderd-worker.conf
install -p -D -m 0600 contrib/confs/rebuilderd.conf %{buildroot}%{_sysconfdir}/rebuilderd.conf
install -p -D -m 0600 contrib/confs/rebuilderd-sync.conf %{buildroot}%{_sysconfdir}/rebuilderd-sync.conf

# man pages
install -p -D -m 0644 contrib/docs/rebuilderd.1 %{buildroot}%{_mandir}/man1/rebuilderd.1
install -p -D -m 0644 contrib/docs/rebuilderd-worker.1 %{buildroot}%{_mandir}/man1/rebuilderd-worker.1
install -p -D -m 0644 contrib/docs/rebuildctl.1 %{buildroot}%{_mandir}/man1/rebuildctl.1

install -p -D -m 0644 contrib/docs/rebuilderd.conf.5 %{buildroot}%{_mandir}/man5/rebuilderd.conf.5
install -p -D -m 0644 contrib/docs/rebuilderd-sync.conf.5 %{buildroot}%{_mandir}/man5/rebuild-sync.conf.5
install -p -D -m 0644 contrib/docs/rebuilderd-worker.conf.5 %{buildroot}%{_mandir}/man5/rebuilderd-worker.conf.5

# generate and install shell completions
target/rpm/rebuildctl completions bash > rebuildctl.bash
target/rpm/rebuildctl completions fish > rebuildctl.fish
target/rpm/rebuildctl completions zsh > _rebuildctl
 
install -Dpm 0644 rebuildctl.bash -t %{buildroot}/%{bash_completions_dir}
install -Dpm 0644 rebuildctl.fish -t %{buildroot}/%{fish_completions_dir}
install -Dpm 0644 _rebuildctl -t %{buildroot}/%{zsh_completions_dir}

%if %{with check}
%check
%cargo_test
%endif

%post
%systemd_post rebuilderd.service
%systemd_post rebuilderd-sync@.service
%systemd_post rebuilderd-sync@.timer

%post worker
%systemd_post rebuilderd-worker.service

%preun
%systemd_preun rebuilderd.service
%systemd_preun rebuilderd-sync@.service
%systemd_preun rebuilderd-sync@.timer

%preun worker
%systemd_preun rebuilderd-worker.service

%postun
%systemd_postun rebuilderd.service

%postun worker
%systemd_postun rebuilderd-worker.service
%systemd_postun rebuilderd-sync@.service
%systemd_postun rebuilderd-sync@.timer

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/rebuilderd

%{_sysusersdir}/rebuilderd.conf
%{_tmpfilesdir}/%{name}.conf

%attr(0640,rebuilderd,rebuilderd) %{_sysconfdir}/rebuilderd.conf
%attr(0640,rebuilderd,rebuilderd) %{_sysconfdir}/rebuilderd-sync.conf

%{_mandir}/man1/rebuilderd.1.*
%{_mandir}/man5/rebuilderd.conf.5.*
%{_mandir}/man5/rebuild-sync.conf.5.*

%{_unitdir}/rebuilderd.service
%{_unitdir}/rebuilderd-sync@.service
%{_unitdir}/rebuilderd-sync@.timer

%files worker
%license LICENSE
%license LICENSE.dependencies
%{_bindir}/rebuilderd-worker
%{_unitdir}/rebuilderd-worker@.service
%config(noreplace) %{_sysconfdir}/rebuilderd-worker.conf
%{_mandir}/man1/rebuilderd-worker.1.*
%{_mandir}/man5/rebuilderd-worker.conf.5.*

%files tools
%license LICENSE
%license LICENSE.dependencies
%{_bindir}/rebuildctl
%{bash_completions_dir}/rebuildctl.bash
%{fish_completions_dir}/rebuildctl.fish
%{zsh_completions_dir}/_rebuildctl
%{_mandir}/man1/rebuildctl.1.*

%changelog
%autochangelog
