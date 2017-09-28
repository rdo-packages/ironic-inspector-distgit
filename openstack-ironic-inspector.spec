%global service ironic-inspector
%global modulename ironic_inspector
%{!?upstream_version: %global upstream_version %{version}}

%global with_doc 1

Name:       openstack-ironic-inspector
Summary:    Hardware introspection service for OpenStack Ironic
Version:    XXX
Release:    XXX
License:    ASL 2.0
URL:        https://launchpad.net/ironic-inspector

Source0:    https://tarballs.openstack.org/%{service}/%{service}-%{version}.tar.gz
Source1:    openstack-ironic-inspector.service
Source2:    openstack-ironic-inspector-dnsmasq.service
Source3:    dnsmasq.conf
Source4:    ironic-inspector-rootwrap-sudoers
Source5:    ironic-inspector.logrotate
Source6:    ironic-inspector-dist.conf

BuildArch:  noarch
BuildRequires: openstack-macros
BuildRequires: python2-devel
BuildRequires: python-pbr
BuildRequires: systemd
# All these are required to run tests during check step
BuildRequires: python-mock
BuildRequires: python-alembic
BuildRequires: python-automaton
BuildRequires: python-babel
BuildRequires: python-construct
BuildRequires: python-eventlet
BuildRequires: python-fixtures
BuildRequires: python-flask
BuildRequires: python-futurist
BuildRequires: python-ironic-lib
BuildRequires: python-ironicclient
BuildRequires: python-jsonpath-rw
BuildRequires: python-jsonschema
BuildRequires: python-keystoneauth1
BuildRequires: python-keystonemiddleware
BuildRequires: python-netaddr
BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-config
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-middleware
BuildRequires: python-oslo-serialization
BuildRequires: python-oslo-utils
BuildRequires: python-oslotest
BuildRequires: python-six
BuildRequires: python-sqlalchemy
BuildRequires: python-stevedore
BuildRequires: python-swiftclient
BuildRequires: python-testscenarios
BuildRequires: python-testresources
BuildRequires: pytz

Requires: dnsmasq
%{?systemd_requires}

Requires: python-pbr
Requires: python-alembic
Requires: python-automaton
Requires: python-babel
Requires: python-construct >= 2.8.10
Requires: python-eventlet
Requires: python-flask
Requires: python-futurist
Requires: python-ironic-lib >= 2.5.0
Requires: python-ironicclient >= 1.14.0
Requires: python-jsonpath-rw
Requires: python-jsonschema
Requires: python-keystoneauth1 >= 3.1.0
Requires: python-keystonemiddleware >= 4.12.0
Requires: python-netaddr
Requires: python-oslo-concurrency >= 3.8.0
Requires: python-oslo-config >= 2:4.0.0
Requires: python-oslo-db >= 4.24.0
Requires: python-oslo-i18n >= 2.1.0
Requires: python-oslo-log >= 3.22.0
Requires: python-oslo-middleware >= 3.27.0
Requires: python-oslo-rootwrap >= 5.0.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-utils >= 3.20.0
Requires: python-six
Requires: python-sqlalchemy
Requires: python-stevedore
Requires: python-swiftclient >= 3.2.0
Requires: pytz

Obsoletes: openstack-ironic-discoverd < 1.1.1
Provides: openstack-ironic-discoverd = %{upstream_version}


%description
Ironic Inspector is an auxiliary service for discovering hardware properties
for a node managed by OpenStack Ironic. Hardware introspection or hardware
properties discovery is a process of getting hardware parameters required for
scheduling from a bare metal node, given it’s power management credentials
(e.g. IPMI address, user name and password).

%if 0%{?with_doc}
%package -n openstack-ironic-inspector-doc
Summary:    Documentation for Ironic Inspector.

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description -n openstack-ironic-inspector-doc
Documentation for Ironic Inspector.
%endif

%package -n python-%{service}-tests
Summary:    %{service} Tempest plugin

Requires:   %{name} = %{version}-%{release}
Requires:   python-tempest >= 12.0.0

%description -n python-%{service}-tests
It contains the unit tests and tempest plugins

%prep
%autosetup -v -p 1 -n %{service}-%{upstream_version}
# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{__python2} setup.py build
%{__python2} setup.py build_sphinx -b html

%install
%{__python2} setup.py install --skip-build --root=%{buildroot}
# Create fake egg-info for the tempest plugin
%py2_entrypoint %{modulename} %{service}

mkdir -p %{buildroot}%{_mandir}/man8
install -p -D -m 644 ironic-inspector.8 %{buildroot}%{_mandir}/man8/

# logs configuration
install -d -m 750 %{buildroot}%{_localstatedir}/log/ironic-inspector
install -d -m 750 %{buildroot}%{_localstatedir}/log/ironic-inspector/ramdisk
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
%{__python2} -m unittest discover ironic_inspector.test.unit

%files
%doc README.rst
%license LICENSE
%config(noreplace) %attr(-,root,ironic-inspector) %{_sysconfdir}/ironic-inspector
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-ironic-inspector
%{_sysconfdir}/sudoers.d/ironic-inspector
%{python2_sitelib}/%{modulename}
%{python2_sitelib}/%{modulename}-*.egg-info
%exclude %{python2_sitelib}/%{modulename}/test
%{_bindir}/ironic-inspector
%{_bindir}/ironic-inspector-rootwrap
%{_bindir}/ironic-inspector-dbsync
%{_unitdir}/openstack-ironic-inspector.service
%{_unitdir}/openstack-ironic-inspector-dnsmasq.service
%attr(-,ironic-inspector,ironic-inspector) %{_sharedstatedir}/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector/ramdisk/
%doc %{_mandir}/man8/ironic-inspector.8.gz
%exclude %{python2_sitelib}/%{modulename}_tests.egg-info

%if 0%{?with_doc}
%files -n openstack-ironic-inspector-doc
%license LICENSE
%doc CONTRIBUTING.rst doc/build/html
%endif

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{modulename}/test
%{python2_sitelib}/%{modulename}_tests.egg-info

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
