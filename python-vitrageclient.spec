%global pypi_name vitrageclient
%if 0%{?fedora}
%global with_python3 1
%else
%global with_python3 0
%endif

%if 0%{?fedora}==0
%global __python2 /usr/bin/python
%endif


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        1.0.1
Release:        3%{?dist}
Summary:        Python client for Vitrage REST API

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Python client for Vitrage REST API. Includes python library for Vitrage API
and Command Line Interface (CLI) library.


%package -n     python2-%{pypi_name}

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires:       python-babel >= 2.3.4
Requires:       python-cliff >= 1.15.0
Requires:       python-keystoneauth1 >= 2.10.0
Requires:       python-pbr
Requires:       python-oslo-utils >= 3.16.0

Requires:       %{name}-bash-completion = %{version}-%{release}

Summary:        Python client for Vitrage REST API
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Python client for Vitrage REST API. Includes python library for Vitrage API
and Command Line Interface (CLI) library.

%if 0%{?with_python3}
# Python3 package
%package -n     python3-%{pypi_name}
Summary:        Python client for Vitrage REST API
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6

Requires:       python3-babel >= 2.3.4
Requires:       python3-cliff >= 1.15.0
Requires:       python3-keystoneauth1 >= 2.10.0
Requires:       python3-pbr
Requires:       python3-oslo-utils >= 3.16.0

%description -n python3-%{pypi_name}
Python client for Vitrage REST API. Includes python library for Vitrage API
and Command Line Interface (CLI) library.
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:       Documentation for python client for Vitrage REST API

BuildRequires: python-sphinx
BuildRequires: python2-oslo-sphinx >= 2.3.0

%description -n python-%{pypi_name}-doc
Documentation for python client for Vitrage REST API. Includes python library
for Vitrage API and Command Line Interface (CLI) library.

%package bash-completion
Summary:        bash completion files for vitrage
BuildRequires:  bash-completion

%description bash-completion
This package contains bash completion files for vitrage.


%prep
%autosetup -n %{name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%if 0%{?with_python3}
%py3_install
# rename python3 binary:
pushd %{buildroot}/%{_bindir}
mv vitrage vitrage-3
ln -s vitrage-3 vitrage-%{python3_version}
popd
%endif

%py2_install

# push autocompletion
bashcompdir=$(pkg-config --variable=completionsdir bash-completion)
mkdir -p %{buildroot}$bashcompdir
mv %{buildroot}%{_datadir}/vitrage.bash_completion %{buildroot}$bashcompdir/vitrage

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/vitrage

%if 0%{?with_python3}
# Files for python3
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/vitrage-3
%{_bindir}/vitrage-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE

%files bash-completion
%license LICENSE
%{_datadir}/bash-completion/completions/vitrage

%changelog
* Fri Nov 04 2016 Matthias Runge <mrunge@redhat.com> - 1.0.1-3
- address review comments (rhbz#1391892)

* Fri Nov 04 2016 Matthias Runge <mrunge@redhat.com> - 1.0.1-2
- fix python3 binary handling and requires
- fix bash-completion handling

* Thu Nov 03 2016 Matthias Runge <mrunge@redhat.com> - 1.0.1-1
- minor spec fixes, py3 conditional, source0 URL

* Tue Sep 27 2016 Marcos Fermin Lobo <lobo@lukos.org> 1.0.1
- First RPM

