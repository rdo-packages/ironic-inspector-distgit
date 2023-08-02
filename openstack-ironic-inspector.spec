%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global service ironic-inspector
%global modulename ironic_inspector
%{!?upstream_version: %global upstream_version %{version}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order os-api-ref
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1
%global with_tests 1

Name:       openstack-ironic-inspector
Summary:    Hardware introspection service for OpenStack Ironic
Version:    XXX
Release:    XXX
License:    Apache-2.0
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
BuildRequires: pyproject-rpm-macros
BuildRequires: systemd
%{?systemd_requires}


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

Requires:   %{name} = %{version}-%{release}

%description -n python3-%{service}-tests
It contains the unit tests

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -v -p 1 -n %{service}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
# Disable warnint-is-error in doc build
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel
%if 0%{?with_doc}
%tox -e docs
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

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
%tox -e %{default_toxenv}
%endif

%files
%doc README.rst
%license LICENSE
%config(noreplace) %attr(-,root,ironic-inspector) %{_sysconfdir}/ironic-inspector
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-ironic-inspector
%{_sysconfdir}/sudoers.d/ironic-inspector
%{python3_sitelib}/%{modulename}
%{python3_sitelib}/%{modulename}-*.dist-info
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
%doc doc/build/html
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

