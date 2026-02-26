# Trustee guest components Quadlet

%global project_name trustee-gc-quadlet
%global project_version 0.1.0

# Build conditional for offline subpackage (disabled by default)
# Enable with: rpmbuild --with offline
%bcond offline 0

Name:           %{project_name}
Version:        %{project_version}
Release:        1%{?dist}
Summary:        Podman Quadlet configurations for Trustee attestation services

License:        Apache-2.0
URL:            https://github.com/confidential-containers/guest-components
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

# Build dependencies
BuildRequires:  systemd-rpm-macros

# Runtime dependencies
Requires:       podman >= 4.4
Requires:       systemd
Requires:       container-selinux
%{?systemd_requires}
%{?systemd_ordering}

%description
Trustee guest components in a Podman Quadlet implementation

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to build

%install
install -d %{buildroot}%{_sysconfdir}/trustee-gc/aa
install -d %{buildroot}%{_sysconfdir}/trustee-gc/cdh

# Install Quadlet files
install -d %{buildroot}%{_datadir}/containers/systemd
install -m 0644 quadlet/*.container %{buildroot}%{_datadir}/containers/systemd/
install -m 0644 quadlet/*.pod %{buildroot}%{_datadir}/containers/systemd/

# Install default configurations
install -m 0644 configs/aa/config.toml %{buildroot}%{_sysconfdir}/trustee-gc/aa/
install -m 0644 configs/cdh/config.toml %{buildroot}%{_sysconfdir}/trustee-gc/cdh/

%post
# Toggle AddDevice=/dev/sev-guest in trustee-gc-aa.container based on availability
AA_CONTAINER="%{_datadir}/containers/systemd/trustee-gc-aa.container"
if [ -e /dev/sev-guest ]; then
  sed -i 's/^#\(AddDevice=\/dev\/sev-guest\)/\1/' "$AA_CONTAINER"
else
  sed -i 's/^\(AddDevice=\/dev\/sev-guest\)/#\1/' "$AA_CONTAINER"
fi
systemctl daemon-reload
%systemd_post trustee-gc-pod.service

%preun
%systemd_preun trustee-gc-pod.service

%postun
%systemd_postun_with_restart trustee-gc-pod.service

%files
%{_datadir}/containers/systemd/trustee-gc-aa.container
%{_datadir}/containers/systemd/trustee-gc-cdh.container
%{_datadir}/containers/systemd/trustee-gc-asr.container
%{_datadir}/containers/systemd/trustee-gc.pod

%dir %{_sysconfdir}/trustee-gc
%dir %{_sysconfdir}/trustee-gc/aa
%dir %{_sysconfdir}/trustee-gc/cdh
%config(noreplace) %{_sysconfdir}/trustee-gc/aa/config.toml
%config(noreplace) %{_sysconfdir}/trustee-gc/cdh/config.toml

%changelog
%autochangelog