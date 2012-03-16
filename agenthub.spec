%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name: agenthub
Version: 0.4
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
Requires: python-webpy
Requires: python-gofer >= 0.66
Requires: python-iniparse
Requires: python-simplejson
Requires: mod_wsgi
Requires: httpd

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
mkdir -p %{buildroot}/srv/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf.d/

cp etc/%{name}/*.conf %{buildroot}/%{_sysconfdir}/%{name}
cp etc/httpd/conf.d/%{name}.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d
cp srv/%{name}/* %{buildroot}/srv/%{name}

rm -rf %{buildroot}/%{python_sitelib}/%{name}*.egg-info

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/conf.d/
%{python_sitelib}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/hub.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(-,apache,apache) /srv/%{name}/*
%attr(-,apache,apache) %{_var}/log/%{name}
%attr(-,apache,apache) %{_var}/lib/%{name}/journal/notify
%doc LICENSE

%changelog
* Fri Mar 16 2012 Jeff Ortel <jortel@redhat.com> 0.4-1
- Change successful asynchronous httpcode (202) Accepted instead of 200.
  (jortel@redhat.com)
- Better exception propagation. (jortel@redhat.com)
- minor renaming. (jortel@redhat.com)
- Do options validation. (jortel@redhat.com)

* Tue Mar 13 2012 Jeff Ortel <jortel@redhat.com> 0.3-1
- deal with optional (body). (jortel@redhat.com)
- Remove debug logging of pid. (jortel@redhat.com)
- Move services startup to bootstrap. (jortel@redhat.com)
- Refactored Services. (jortel@redhat.com)

* Tue Mar 13 2012 Jeff Ortel <jortel@redhat.com> 0.2-1
- better http/exception mapping and improved BadRequest() messages.
  (jortel@redhat.com)

* Tue Mar 13 2012 Jeff Ortel <jortel@redhat.com> 0.1-1
- new package built with tito

