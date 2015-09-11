%global pypi_name ironic-inspector
%{!?upstream_version: %global upstream_version %{version}}

Name:       openstack-ironic-inspector
Summary:    Hardware introspection service for OpenStack Ironic
Version:    2.1.0
Release:    1%{?dist}
License:    ASL 2.0
URL:        https://launchpad.net/ironic-inspector

Source0:    https://pypi.python.org/packages/source/i/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:    openstack-ironic-inspector.service
Source2:    openstack-ironic-inspector-dnsmasq.service
Source3:    dnsmasq.conf

BuildArch:  noarch
BuildRequires: python2-devel
BuildRequires: python-pbr
BuildRequires: systemd
# All these are required to run tests during check step
BuildRequires: python-mock
BuildRequires: python-babel
BuildRequires: python-eventlet
BuildRequires: python-flask
BuildRequires: python-ironicclient
BuildRequires: python-keystoneclient
BuildRequires: python-keystonemiddleware
BuildRequires: python-oslo-config
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-utils
BuildRequires: python-six
BuildRequires: python-stevedore
BuildRequires: python-swiftclient

Requires: dnsmasq
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: python-babel
Requires: python-eventlet
Requires: python-flask
Requires: python-ironicclient
Requires: python-keystoneclient
Requires: python-keystonemiddleware
Requires: python-oslo-config
Requires: python-oslo-db
Requires: python-oslo-i18n
Requires: python-oslo-log
Requires: python-oslo-utils
Requires: python-six
Requires: python-stevedore
Requires: python-swiftclient

Obsoletes: openstack-ironic-discoverd < 1.1.0-3
Provides: openstack-ironic-discoverd = %{version}-%{release}
Obsoletes: python-ironic-discoverd < 1.1.0-3
Provides: python-ironic-discoverd = %{version}-%{release}


%description
Ironic Inspector is an auxiliary service for discovering hardware properties
for a node managed by OpenStack Ironic. Hardware introspection or hardware
properties discovery is a process of getting hardware parameters required for
scheduling from a bare metal node, given it’s power management credentials
(e.g. IPMI address, user name and password).

%package -n openstack-ironic-inspector-doc
Summary:    Documentation for Ironic Inspector.

%description -n openstack-ironic-inspector-doc
Documentation for Ironic Inspector.

%prep
%autosetup -v -p 1 -n %{pypi_name}-%{upstream_version}
rm -rf *.egg-info
# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,plugin-,}requirements.txt

%build
%py2_build

%install
%py2_install
mkdir -p %{buildroot}%{_mandir}/man8
install -p -D -m 644 ironic-inspector.8 %{buildroot}%{_mandir}/man8/

# install systemd scripts
mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}

# configuration contains passwords, thus 640
install -p -D -m 640 example.conf %{buildroot}/%{_sysconfdir}/ironic-inspector/inspector.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/ironic-inspector/dnsmasq.conf

%check
%{__python2} -m unittest discover ironic_inspector.test

%files
%doc README.rst
%license LICENSE
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/ironic-inspector
%{python2_sitelib}/ironic_inspector*
%{python2_sitelib}/ironic_inspector-*.egg-info
%{_bindir}/ironic-inspector
%{_unitdir}/openstack-ironic-inspector.service
%{_unitdir}/openstack-ironic-inspector-dnsmasq.service
%doc %{_mandir}/man8/ironic-inspector.8.gz

%files -n openstack-ironic-inspector-doc
%license LICENSE
%doc CONTRIBUTING.rst HTTP-API.rst

%post
%systemd_post openstack-ironic-inspector.service
%systemd_post openstack-ironic-inspector-dnsmasq.service

%preun
%systemd_preun openstack-ironic-inspector.service
%systemd_preun openstack-ironic-inspector-dnsmasq.service

%postun
%systemd_postun_with_restart openstack-ironic-inspector.service
%systemd_postun_with_restart openstack-ironic-inspector-dnsmasq.service


%changelog
* Fri Sep 11 2015 John Trowbridge <trown@redhat.com> - 2.1.0-1
- Rename from openstack-ironic-discoverd 1.1.0-3
