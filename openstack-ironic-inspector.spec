%global service ironic-inspector
%{!?upstream_version: %global upstream_version %{version}}

Name:       openstack-ironic-inspector
Summary:    Hardware introspection service for OpenStack Ironic
Version:    3.2.2
Release:    1%{?dist}
License:    ASL 2.0
URL:        https://launchpad.net/ironic-inspector

Source0:    http://tarballs.openstack.org/%{service}/%{service}-%{version}.tar.gz
Source1:    openstack-ironic-inspector.service
Source2:    openstack-ironic-inspector-dnsmasq.service
Source3:    dnsmasq.conf
Source4:    ironic-inspector-rootwrap-sudoers
Source5:    ironic-inspector.logrotate
Source6:    ironic-inspector-dist.conf

BuildArch:  noarch
BuildRequires: python2-devel
BuildRequires: python-pbr
BuildRequires: systemd
# All these are required to run tests during check step
BuildRequires: python-mock
BuildRequires: python-babel
BuildRequires: python-eventlet
BuildRequires: python-fixtures
BuildRequires: python-flask
BuildRequires: python-futurist
BuildRequires: python-ironicclient
BuildRequires: python-jsonpath-rw
BuildRequires: python-jsonschema
BuildRequires: python-keystoneclient
BuildRequires: python-keystonemiddleware
BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-config
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-middleware
BuildRequires: python-oslo-sphinx
BuildRequires: python-oslo-utils
BuildRequires: python-oslotest
BuildRequires: python-six
BuildRequires: python-sphinx
BuildRequires: python-stevedore
BuildRequires: python-swiftclient
BuildRequires: python-testscenarios
BuildRequires: python-testresources

Requires: dnsmasq
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: python-babel
Requires: python-eventlet
Requires: python-flask
Requires: python-futurist
Requires: python-ironicclient
Requires: python-jsonpath-rw
Requires: python-jsonschema
Requires: python-keystoneclient
Requires: python-keystonemiddleware
Requires: python-oslo-concurrency
Requires: python-oslo-config
Requires: python-oslo-db
Requires: python-oslo-i18n
Requires: python-oslo-log
Requires: python-oslo-middleware
Requires: python-oslo-rootwrap
Requires: python-oslo-utils
Requires: python-six
Requires: python-stevedore
Requires: python-swiftclient

Obsoletes: openstack-ironic-discoverd < 1.1.1
Provides: openstack-ironic-discoverd = %{upstream_version}


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
%autosetup -v -p 1 -n %{service}-%{upstream_version}
# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,plugin-,}requirements.txt

%build
%{__python2} setup.py build
%{__python2} setup.py build_sphinx

%install
%{__python2} setup.py install --skip-build --root=%{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8
install -p -D -m 644 ironic-inspector.8 %{buildroot}%{_mandir}/man8/

# logs configuration
mkdir -p %{buildroot}%{_localstatedir}/log/ironic-inspector/ramdisk/
install -p -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-ironic-inspector

# install systemd scripts
mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}

# install sudoers file
mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d
install -p -D -m 440 %{SOURCE4} %{buildroot}%{_sysconfdir}/sudoers.d/ironic-inspector

# configuration contains passwords, thus 640
install -p -D -m 640 example.conf %{buildroot}/%{_sysconfdir}/ironic-inspector/inspector.conf
install -p -D -m 640 %{SOURCE6} %{buildroot}/%{_sysconfdir}/ironic-inspector/inspector-dist.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/ironic-inspector/dnsmasq.conf

# rootwrap configuration
mkdir -p %{buildroot}%{_sysconfdir}/ironic-inspector/rootwrap.d
install -p -D -m 640 rootwrap.conf %{buildroot}/%{_sysconfdir}/ironic-inspector/rootwrap.conf
install -p -D -m 640 rootwrap.d/* %{buildroot}/%{_sysconfdir}/ironic-inspector/rootwrap.d/

# shared state directory for sqlite database
mkdir -p %{buildroot}%{_sharedstatedir}/ironic-inspector

%check
%{__python2} -m unittest discover ironic_inspector.test

%files
%doc README.rst
%license LICENSE
%config(noreplace) %attr(-,root,ironic-inspector) %{_sysconfdir}/ironic-inspector
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-ironic-inspector
%{_sysconfdir}/sudoers.d/ironic-inspector
%{python2_sitelib}/ironic_inspector*
%{_bindir}/ironic-inspector
%{_bindir}/ironic-inspector-rootwrap
%{_bindir}/ironic-inspector-dbsync
%{_unitdir}/openstack-ironic-inspector.service
%{_unitdir}/openstack-ironic-inspector-dnsmasq.service
%attr(-,ironic-inspector,ironic-inspector) %{_sharedstatedir}/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector/ramdisk/
%doc %{_mandir}/man8/ironic-inspector.8.gz

%files -n openstack-ironic-inspector-doc
%license LICENSE
%doc CONTRIBUTING.rst doc/build/html

%pre
getent group ironic-inspector >/dev/null || groupadd -r ironic-inspector
getent passwd ironic-inspector >/dev/null || \
    useradd -r -g ironic-inspector -d %{_sharedstatedir}/ironic-inspector -s /sbin/nologin \
-c "OpenStack Ironic Inspector Daemons" ironic-inspector
exit 0

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
* Fri Jun 17 2016 Haikel Guemar <hguemar@fedoraproject.org> 3.2.2-1
- Update to 3.2.2

* Thu May 26 2016 Haikel Guemar <hguemar@fedoraproject.org> 3.2.1-1
- Update to 3.2.1

* Wed Mar 30 2016 RDO <rdo-list@redhat.com> 3.2.0-0.1
- RC1 Rebuild for Mitaka RC1 
