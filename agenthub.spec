%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name: agenthub
Version: 0.3
Release: 1%{?dist}
Summary: The Gofer server
Group:   Development/Languages
License: LGPLv2
URL: https://fedorahosted.org/agenthub/
Source0: https://fedorahosted.org/releases/a/g/agenthub/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: rpm-python
Requires: python-%{name} = %{version}
Requires: python-iniparse
%description
The rest hub is a gofer server that provides gofer services aggregation
that is exposed through a REST API.

%prep
%setup -q

%build
pushd src
%{__python} setup.py build
popd

%install
rm -rf %{buildroot}
pushd src
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/conf.d
mkdir -p %{buildroot}/%{_var}/log/%{name}
mkdir -p %{buildroot}/%{_var}/lib/%{name}/journal/notify

cp etc/%{name}/*.conf %{buildroot}/%{_sysconfdir}/%{name}

rm -rf %{buildroot}/%{python_sitelib}/%{name}*.egg-info

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/conf.d/
%{python_sitelib}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/hub.conf
%{_var}/log/%{name}
%doc LICENSE

%changelog
* Tue Mar 13 2012 Jeff Ortel <jortel@redhat.com> 0.3-1
- Add LICENSE file. (jortel@redhat.com)

* Tue Mar 13 2012 Jeff Ortel <jortel@redhat.com> 0.2-1
- new package built with tito

