#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	pyClamd
Summary:	A python interface to Clamd (Clamav daemon)
# Name must match the python module/package name (as in 'import' statement)
Name:		python-%{module}
Version:	0.3.10
Release:	3
License:	- (enter GPL/GPL v2/GPL v3/LGPL/BSD/BSD-like/other license name here)
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/pyClamd/%{module}-%{version}.tar.gz
# Source0-md5:	370d7c12da34376eca730aea193a8712
URL:		http://xael.org/norman/python/pyclamd/
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pyClamd is a python interface to Clamd (Clamav daemon). By using
pyClamd, you can add virus detection capabilities to your python
software in an efficient and easy way.

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
pyClamd is a python interface to Clamd (Clamav daemon). By using
pyClamd, you can add virus detection capabilities to your python
software in an efficient and easy way.

%prep
%setup -q -n %{module}-%{version}

sed -i -e 's#/etc/clamav/clamd.conf#/etc/clamd.conf#g' README.txt pyclamd/pyclamd.py

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.txt
%dir %{py_sitescriptdir}/pyclamd
%{py_sitescriptdir}/pyclamd/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.txt
%{py3_sitescriptdir}/pyclamd
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
