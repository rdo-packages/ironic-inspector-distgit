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
BuildRequires: python2-pbr
BuildRequires: systemd
# All these are required to run tests during check step
BuildRequires: python2-mock
BuildRequires: python2-alembic
BuildRequires: python2-automaton
BuildRequires: python2-babel
BuildRequires: python-construct
BuildRequires: python2-eventlet
BuildRequires: python2-fixtures
BuildRequires: python-flask
BuildRequires: python2-futurist
BuildRequires: python-ironic-lib
BuildRequires: python2-ironicclient
BuildRequires: python-jsonpath-rw
BuildRequires: python2-jsonschema
BuildRequires: python2-keystoneauth1
BuildRequires: python2-keystonemiddleware
BuildRequires: python2-netaddr
BuildRequires: python2-oslo-concurrency
BuildRequires: python2-oslo-config
BuildRequires: python2-oslo-context
BuildRequires: python2-oslo-db
BuildRequires: python2-oslo-i18n
BuildRequires: python2-oslo-log
BuildRequires: python2-oslo-middleware
BuildRequires: python2-oslo-policy
BuildRequires: python2-oslo-serialization
BuildRequires: python2-oslo-utils
BuildRequires: python2-oslotest
BuildRequires: python-retrying
BuildRequires: python2-six
BuildRequires: python2-sqlalchemy
BuildRequires: python2-stevedore
BuildRequires: python2-swiftclient
BuildRequires: python2-testscenarios
BuildRequires: python2-testresources
BuildRequires: pytz

Requires: dnsmasq
%{?systemd_requires}

Requires: python2-pbr
Requires: python2-alembic
Requires: python2-automaton
Requires: python2-babel
Requires: python-construct >= 2.8.10
Requires: python2-eventlet
Requires: python-flask
Requires: python2-futurist
Requires: python-ironic-lib >= 2.5.0
Requires: python2-ironicclient >= 1.14.0
Requires: python-jsonpath-rw
Requires: python2-jsonschema
Requires: python2-keystoneauth1 >= 3.3.0
Requires: python2-keystonemiddleware >= 4.17.0
Requires: python2-netaddr
Requires: python2-oslo-concurrency >= 3.25.0
Requires: python2-oslo-config >= 2:5.1.0
Requires: python2-oslo-context >= 2.19.2
Requires: python2-oslo-db >= 4.27.0
Requires: python2-oslo-i18n >= 3.15.3
Requires: python2-oslo-log >= 3.36.0
Requires: python2-oslo-middleware >= 3.31.0
Requires: python2-oslo-policy >= 1.30.0
Requires: python2-oslo-rootwrap >= 5.8.0
Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python-retrying >= 1.2.3
Requires: python2-six
Requires: python2-sqlalchemy
Requires: python2-stevedore
Requires: python2-swiftclient >= 3.2.0
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

BuildRequires: python2-sphinx
BuildRequires: python2-oslo-sphinx

%description -n openstack-ironic-inspector-doc
Documentation for Ironic Inspector.
%endif

%package -n python2-%{service}-tests
Summary:    %{service} Unit Tests
%{?python_provide:%python_provide python2-%{service}-tests}

Requires:   %{name} = %{version}-%{release}

%description -n python2-%{service}-tests
It contains the unit tests

%prep
%autosetup -v -p 1 -n %{service}-%{upstream_version}
# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{__python2} setup.py build
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
%endif

%install
%{__python2} setup.py install --skip-build --root=%{buildroot}

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

# generate example configuration files
install -d -m 750 %{buildroot}%{_sysconfdir}/ironic-inspector
export PYTHONPATH=.
oslo-config-generator --config-file config-generator.conf --output-file %{buildroot}/%{_sysconfdir}/ironic-inspector/inspector.conf
oslopolicy-sample-generator --config-file policy-generator.conf --output-file %{buildroot}/%{_sysconfdir}/ironic-inspector/policy.json

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
%attr(-,ironic-inspector,ironic-inspector) %{_sharedstatedir}/ironic-inspector/dhcp-hostsdir
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector/ramdisk/
%doc %{_mandir}/man8/ironic-inspector.8.gz
%exclude %{python2_sitelib}/%{modulename}_tests.egg-info

%if 0%{?with_doc}
%files -n openstack-ironic-inspector-doc
%license LICENSE
%doc CONTRIBUTING.rst doc/build/html
%endif

%files -n python2-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{modulename}/test

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
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/ironic-inspector/commit/?id=c6ad0f0ead6cbb97a1adf053489fee45adeeca33
