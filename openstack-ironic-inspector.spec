# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global service ironic-inspector
%global modulename ironic_inspector
%{!?upstream_version: %global upstream_version %{version}}

%global with_doc 1
%global with_tests 1

Name:       openstack-ironic-inspector
Summary:    Hardware introspection service for OpenStack Ironic
Version:    9.2.1
Release:    1%{?dist}
License:    ASL 2.0
URL:        https://launchpad.net/ironic-inspector

Source0:    https://tarballs.openstack.org/%{service}/%{service}-%{version}.tar.gz
Source1:    openstack-ironic-inspector.service
Source2:    openstack-ironic-inspector-dnsmasq.service
Source3:    dnsmasq.conf
Source4:    ironic-inspector-rootwrap-sudoers
Source5:    ironic-inspector.logrotate
Source6:    ironic-inspector-dist.conf
Source7:    openstack-ironic-inspector-conductor.service

BuildArch:  noarch
BuildRequires: git
BuildRequires: openstack-macros
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-pbr
BuildRequires: python%{pyver}-stestr
BuildRequires: systemd
# All these are required to run tests during check step
BuildRequires: python%{pyver}-mock >= 3.0.5
BuildRequires: python%{pyver}-alembic
BuildRequires: python%{pyver}-automaton
BuildRequires: python%{pyver}-babel
BuildRequires: python%{pyver}-eventlet
BuildRequires: python%{pyver}-fixtures
BuildRequires: python%{pyver}-futurist
BuildRequires: python%{pyver}-ironicclient
BuildRequires: python%{pyver}-jsonschema
BuildRequires: python%{pyver}-keystoneauth1
BuildRequires: python%{pyver}-keystonemiddleware
BuildRequires: python%{pyver}-netaddr
BuildRequires: python%{pyver}-oslo-concurrency
BuildRequires: python%{pyver}-oslo-config
BuildRequires: python%{pyver}-oslo-context
BuildRequires: python%{pyver}-oslo-db
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-oslo-log
BuildRequires: python%{pyver}-oslo-messaging
BuildRequires: python%{pyver}-oslo-middleware
BuildRequires: python%{pyver}-oslo-policy
BuildRequires: python%{pyver}-oslo-serialization
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-six
BuildRequires: python%{pyver}-sqlalchemy
BuildRequires: python%{pyver}-stevedore
BuildRequires: python%{pyver}-openstacksdk
BuildRequires: python%{pyver}-testscenarios
BuildRequires: python%{pyver}-testresources
BuildRequires: python%{pyver}-tooz

%{?systemd_requires}

Requires: python%{pyver}-pbr
Requires: python%{pyver}-alembic
Requires: python%{pyver}-automaton
Requires: python%{pyver}-babel
Requires: python%{pyver}-eventlet
Requires: python%{pyver}-futurist
Requires: python%{pyver}-ironicclient >= 2.3.0
Requires: python%{pyver}-jsonschema
Requires: python%{pyver}-keystoneauth1 >= 3.4.0
Requires: python%{pyver}-keystonemiddleware >= 4.18.0
Requires: python%{pyver}-netaddr
Requires: python%{pyver}-oslo-concurrency >= 3.26.0
Requires: python%{pyver}-oslo-config >= 2:5.2.0
Requires: python%{pyver}-oslo-context >= 2.19.2
Requires: python%{pyver}-oslo-db >= 4.27.0
Requires: python%{pyver}-oslo-i18n >= 3.15.3
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-messaging >= 5.32.0
Requires: python%{pyver}-oslo-middleware >= 3.31.0
Requires: python%{pyver}-oslo-policy >= 1.30.0
Requires: python%{pyver}-oslo-rootwrap >= 5.8.0
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-service >= 1.24.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-six
Requires: python%{pyver}-sqlalchemy
Requires: python%{pyver}-stevedore
Requires: python%{pyver}-tooz >= 1.64.0
Requires: python%{pyver}-openstacksdk >= 0.30.0

# Handle python2 exception
%if %{pyver} == 2
Requires: python-construct >= 2.8.10
Requires: python-flask
Requires: python-ironic-lib >= 2.17.0
Requires: python-jsonpath-rw
Requires: python-retrying >= 1.2.3
Requires: pytz
%else
Requires: python%{pyver}-construct >= 2.8.10
Requires: python%{pyver}-flask
Requires: python%{pyver}-ironic-lib >= 2.17.0
Requires: python%{pyver}-jsonpath-rw
Requires: python%{pyver}-retrying >= 1.2.3
Requires: python%{pyver}-pytz
%endif
# Handle python2 exception
%if %{pyver} == 2
BuildRequires: python-construct
BuildRequires: python-flask
BuildRequires: python-ironic-lib
BuildRequires: python-jsonpath-rw
BuildRequires: python-retrying
BuildRequires: pytz
%else
BuildRequires: python%{pyver}-construct
BuildRequires: python%{pyver}-flask
BuildRequires: python%{pyver}-ironic-lib
BuildRequires: python%{pyver}-jsonpath-rw
BuildRequires: python%{pyver}-retrying
BuildRequires: python%{pyver}-pytz
%endif

Obsoletes: openstack-ironic-discoverd < 1.1.1
Provides: openstack-ironic-discoverd = %{upstream_version}

# NOTE(dtantsur): provide this as a temporary compatibility measure until we
# update all consumers. Can it be handled more gracefully?
Requires:   openstack-ironic-inspector-dnsmasq = %{version}-%{release}

%description
Ironic Inspector is an auxiliary service for discovering hardware properties
for a node managed by OpenStack Ironic. Hardware introspection or hardware
properties discovery is a process of getting hardware parameters required for
scheduling from a bare metal node, given it’s power management credentials
(e.g. IPMI address, user name and password).

This package contains Python modules and an ironic-inspector service combining
API and conductor in one binary.

%if 0%{?with_doc}
%package -n openstack-ironic-inspector-doc
Summary:    Documentation for Ironic Inspector.

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-sphinxcontrib-rsvgconverter

%description -n openstack-ironic-inspector-doc
Documentation for Ironic Inspector.
%endif

%package -n openstack-ironic-inspector-dnsmasq
Summary:    DHCP service for ironic-inspector using dnsmasq

Requires:   %{name} = %{version}-%{release}
Requires:   dnsmasq

%description -n openstack-ironic-inspector-dnsmasq
Ironic Inspector is an auxiliary service for discovering hardware properties
for a node managed by OpenStack Ironic. Hardware introspection or hardware
properties discovery is a process of getting hardware parameters required for
scheduling from a bare metal node, given it’s power management credentials
(e.g. IPMI address, user name and password).

This package contains a dnsmasq service pre-configured for using with
ironic-inspector.

%package -n openstack-ironic-inspector-conductor
Summary:    Conductor service for Ironic Inspector.

Requires:   %{name} = %{version}-%{release}

%description -n openstack-ironic-inspector-conductor
Ironic Inspector is an auxiliary service for discovering hardware properties
for a node managed by OpenStack Ironic. Hardware introspection or hardware
properties discovery is a process of getting hardware parameters required for
scheduling from a bare metal node, given it’s power management credentials
(e.g. IPMI address, user name and password).

This package contains an ironic-inspector conductor service, which can be used
to split ironic-inspector into API and conductor processes.

%package -n openstack-ironic-inspector-api
Summary:    WSGI service service for Ironic Inspector.

Requires:   %{name} = %{version}-%{release}

%description -n openstack-ironic-inspector-api
Ironic Inspector is an auxiliary service for discovering hardware properties
for a node managed by OpenStack Ironic. Hardware introspection or hardware
properties discovery is a process of getting hardware parameters required for
scheduling from a bare metal node, given it’s power management credentials
(e.g. IPMI address, user name and password).

This package contains an ironic-inspector WSGI service, which can be used
to split ironic-inspector into API and conductor processes.

%package -n python%{pyver}-%{service}-tests
Summary:    %{service} Unit Tests
%{?python_provide:%python_provide python2-%{service}-tests}

Requires:   %{name} = %{version}-%{release}

%description -n python%{pyver}-%{service}-tests
It contains the unit tests

%prep
%autosetup -v -p 1 -n %{service}-%{upstream_version} -S git
# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pyver_build}
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
%endif

%install
%{pyver_install}

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
install -p -D -m 644 %{SOURCE7} %{buildroot}%{_unitdir}

# install sudoers file
mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d
install -p -D -m 440 %{SOURCE4} %{buildroot}%{_sysconfdir}/sudoers.d/ironic-inspector

# generate example configuration files
install -d -m 750 %{buildroot}%{_sysconfdir}/ironic-inspector
export PYTHONPATH=.
oslo-config-generator-%{pyver} --config-file tools/config-generator.conf --output-file %{buildroot}/%{_sysconfdir}/ironic-inspector/inspector.conf
oslopolicy-sample-generator-%{pyver} --config-file tools/policy-generator.conf --output-file %{buildroot}/%{_sysconfdir}/ironic-inspector/policy.json

# configuration contains passwords, thus 640
chmod 0640 %{buildroot}/%{_sysconfdir}/ironic-inspector/inspector.conf
install -p -D -m 640 %{SOURCE6} %{buildroot}/%{_sysconfdir}/ironic-inspector/inspector-dist.conf
install -p -D -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/ironic-inspector/dnsmasq.conf

# rootwrap configuration
mkdir -p %{buildroot}%{_sysconfdir}/ironic-inspector/rootwrap.d
install -p -D -m 640 rootwrap.conf %{buildroot}/%{_sysconfdir}/ironic-inspector/rootwrap.conf
install -p -D -m 640 rootwrap.d/* %{buildroot}/%{_sysconfdir}/ironic-inspector/rootwrap.d/

# shared state directory
mkdir -p %{buildroot}%{_sharedstatedir}/ironic-inspector

# shared state directory for the dnsmasq PXE filter and the dnsmasq service
mkdir -p %{buildroot}%{_sharedstatedir}/ironic-inspector/dhcp-hostsdir


%check
%if 0%{?with_tests}
PYTHON=%{pyver_bin} stestr-%{pyver} run --test-path ironic_inspector.test.unit
%endif

%files
%doc README.rst
%license LICENSE
%config(noreplace) %attr(-,root,ironic-inspector) %{_sysconfdir}/ironic-inspector
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-ironic-inspector
%{_sysconfdir}/sudoers.d/ironic-inspector
%{pyver_sitelib}/%{modulename}
%{pyver_sitelib}/%{modulename}-*.egg-info
%exclude %{pyver_sitelib}/%{modulename}/test
%{_bindir}/ironic-inspector
%{_bindir}/ironic-inspector-rootwrap
%{_bindir}/ironic-inspector-dbsync
%{_bindir}/ironic-inspector-migrate-data
%{_unitdir}/openstack-ironic-inspector.service
%attr(-,ironic-inspector,ironic-inspector) %{_sharedstatedir}/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_sharedstatedir}/ironic-inspector/dhcp-hostsdir
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector/ramdisk/
%doc %{_mandir}/man8/ironic-inspector.8.gz
%exclude %{pyver_sitelib}/%{modulename}_tests.egg-info

%if 0%{?with_doc}
%files -n openstack-ironic-inspector-doc
%license LICENSE
%doc CONTRIBUTING.rst doc/build/html
%endif

%files -n openstack-ironic-inspector-dnsmasq
%license LICENSE
%{_unitdir}/openstack-ironic-inspector-dnsmasq.service

%files -n openstack-ironic-inspector-conductor
%license LICENSE
%{_bindir}/ironic-inspector-conductor
%{_unitdir}/openstack-ironic-inspector-conductor.service

%files -n openstack-ironic-inspector-api
%license LICENSE
%{_bindir}/ironic-inspector-api-wsgi

%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{modulename}/test

%pre
getent group ironic-inspector >/dev/null || groupadd -r ironic-inspector
getent passwd ironic-inspector >/dev/null || \
    useradd -r -g ironic-inspector -d %{_sharedstatedir}/ironic-inspector -s /sbin/nologin \
-c "OpenStack Ironic Inspector Daemons" ironic-inspector
exit 0

%post
%systemd_post openstack-ironic-inspector.service

%post -n openstack-ironic-inspector-dnsmasq
%systemd_post openstack-ironic-inspector-dnsmasq.service

%post -n openstack-ironic-inspector-conductor
%systemd_post openstack-ironic-inspector-conductor.service

%preun
%systemd_preun openstack-ironic-inspector.service

%preun -n openstack-ironic-inspector-dnsmasq
%systemd_preun openstack-ironic-inspector-dnsmasq.service

%preun -n openstack-ironic-inspector-conductor
%systemd_preun openstack-ironic-inspector-conductor.service

%postun
%systemd_postun_with_restart openstack-ironic-inspector.service

%postun -n openstack-ironic-inspector-dnsmasq
%systemd_postun_with_restart openstack-ironic-inspector-dnsmasq.service

%postun -n openstack-ironic-inspector-conductor
%systemd_postun_with_restart openstack-ironic-inspector-conductor.service

%changelog
* Fri Feb 07 2020 RDO <dev@lists.rdoproject.org> 9.2.1-1
- Update to 9.2.1

* Mon Sep 30 2019 RDO <dev@lists.rdoproject.org> 9.2.0-1
- Update to 9.2.0

