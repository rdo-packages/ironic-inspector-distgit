%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global service ironic-inspector
%global modulename ironic_inspector
%{!?upstream_version: %global upstream_version %{version}}

%global with_doc 1
%global with_tests 1

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
Source7:    openstack-ironic-inspector-conductor.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires: git-core
BuildRequires: openstack-macros
BuildRequires: python3-devel
BuildRequires: python3-pbr
BuildRequires: python3-stestr
BuildRequires: systemd
# All these are required to run tests during check step
BuildRequires: python3-mock >= 3.0.5
BuildRequires: python3-alembic
BuildRequires: python3-automaton
BuildRequires: python3-eventlet
BuildRequires: python3-fixtures
BuildRequires: python3-futurist
BuildRequires: python3-ironicclient
BuildRequires: python3-jsonschema
BuildRequires: python3-keystoneauth1
BuildRequires: python3-keystonemiddleware
BuildRequires: python3-netaddr
BuildRequires: python3-oslo-concurrency
BuildRequires: python3-oslo-config
BuildRequires: python3-oslo-context
BuildRequires: python3-oslo-db
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-log
BuildRequires: python3-oslo-messaging
BuildRequires: python3-oslo-middleware
BuildRequires: python3-oslo-policy
BuildRequires: python3-oslo-serialization
BuildRequires: python3-oslo-utils
BuildRequires: python3-oslotest
BuildRequires: python3-six
BuildRequires: python3-sqlalchemy
BuildRequires: python3-stevedore
BuildRequires: python3-openstacksdk
BuildRequires: python3-testscenarios
BuildRequires: python3-testresources
BuildRequires: python3-tooz
BuildRequires: python3-construct
BuildRequires: python3-flask
BuildRequires: python3-ironic-lib
BuildRequires: python3-jsonpath-rw
BuildRequires: python3-retrying
BuildRequires: python3-pytz

%{?systemd_requires}

Requires: python3-alembic >= 1.4.2
Requires: python3-automaton >= 1.9.0
Requires: python3-construct >= 2.9.39
Requires: python3-eventlet >= 0.26.0
Requires: python3-flask >= 1:1.1.0
Requires: python3-futurist >= 1.2.0
Requires: python3-ironic-lib >= 4.3.0
Requires: python3-jsonpath-rw >= 1.2.0
Requires: python3-jsonschema >= 3.2.0
Requires: python3-keystoneauth1 >= 4.2.0
Requires: python3-keystonemiddleware >= 4.18.0
Requires: python3-netaddr >= 0.7.18
Requires: python3-openstacksdk >= 0.40.0
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-config >= 2:6.8.0
Requires: python3-oslo-context >= 2.22.0
Requires: python3-oslo-db >= 12.1.0
Requires: python3-oslo-i18n >= 3.20.0
Requires: python3-oslo-log >= 4.3.0
Requires: python3-oslo-messaging >= 14.1.0
Requires: python3-oslo-middleware >= 3.31.0
Requires: python3-oslo-policy >= 3.7.0
Requires: python3-oslo-rootwrap >= 5.8.0
Requires: python3-oslo-serialization >= 2.25.0
Requires: python3-oslo-service >= 1.31.0
Requires: python3-oslo-utils >= 4.5.0
Requires: python3-pbr >= 3.1.1
Requires: python3-pytz >= 2013.6
Requires: python3-sqlalchemy >= 1.4.0
Requires: python3-stevedore >= 1.20.0
Requires: python3-tooz >= 2.5.1
Requires: python3-tenacity >= 6.2.0
Requires: python3-yaml >= 5.3.1
Requires: python3-oslo-upgradecheck >= 1.2.0


Obsoletes: openstack-ironic-discoverd < 1.1.1
Provides: openstack-ironic-discoverd = %{upstream_version}

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

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme
BuildRequires: python3-sphinxcontrib-apidoc
BuildRequires: python3-sphinxcontrib-rsvgconverter

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

%package -n python3-%{service}-tests
Summary:    %{service} Unit Tests
%{?python_provide:%python_provide python2-%{service}-tests}

Requires:   %{name} = %{version}-%{release}

%description -n python3-%{service}-tests
It contains the unit tests

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -v -p 1 -n %{service}-%{upstream_version} -S git
# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}
%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

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
oslo-config-generator --config-file tools/config-generator.conf --output-file %{buildroot}/%{_sysconfdir}/ironic-inspector/inspector.conf
oslopolicy-sample-generator --config-file tools/policy-generator.conf --output-file %{buildroot}/%{_sysconfdir}/ironic-inspector/policy.json

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
PYTHON=%{__python3} stestr run --test-path ironic_inspector.test.unit
%endif

%files
%doc README.rst
%license LICENSE
%config(noreplace) %attr(-,root,ironic-inspector) %{_sysconfdir}/ironic-inspector
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-ironic-inspector
%{_sysconfdir}/sudoers.d/ironic-inspector
%{python3_sitelib}/%{modulename}
%{python3_sitelib}/%{modulename}-*.egg-info
%exclude %{python3_sitelib}/%{modulename}/test
%{_bindir}/ironic-inspector
%{_bindir}/ironic-inspector-rootwrap
%{_bindir}/ironic-inspector-dbsync
%{_bindir}/ironic-inspector-status
%{_bindir}/ironic-inspector-migrate-data
%{_unitdir}/openstack-ironic-inspector.service
%attr(-,ironic-inspector,ironic-inspector) %{_sharedstatedir}/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_sharedstatedir}/ironic-inspector/dhcp-hostsdir
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector
%attr(-,ironic-inspector,ironic-inspector) %{_localstatedir}/log/ironic-inspector/ramdisk/
%doc %{_mandir}/man8/ironic-inspector.8.gz
%exclude %{python3_sitelib}/%{modulename}_tests.egg-info

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

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{modulename}/test

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

