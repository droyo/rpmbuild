Name:         s6
Version:      1.0.0
Release:      1
License:      ISC
Source:       http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Summary:      Process supervision suite
Group:        System Environment/Daemons
BuildRequires: /usr/bin/musl-gcc skalibs execline

%description
s6 is a small suite of programs for UNIX, designed to allow process supervision
(a.k.a service supervision), in the line of daemontools and runit.

%prep
%setup -q -n admin/%{name}-%{version}

%build
rm -rf %{buildroot}
pushd conf-compile
touch flag-allstatic
rm -f flag-slashpackage
echo 'musl-gcc'                 > conf-cc
echo 'musl-gcc -static'         > conf-ld
echo 'musl-gcc'                 > conf-dynld
echo %{_includedir}/skalibs                 > path-include
echo %{_libdir}/skalibs                     > path-library
echo /%{_lib}                               > path-library.so
echo %{_libdir}/skalibs/sysdeps             > import
echo %{buildroot}%{_bindir}                 > conf-install-command
echo %{buildroot}%{_libdir}                 > conf-install-library
echo %{buildroot}%{_includedir}             > conf-install-include
echo %{buildroot}/%{_lib}                   > conf-install-library.so
echo %{buildroot}%{_sysconfdir}             > conf-install-etc

popd

%install

make install
mkdir -p %{buildroot}%{_sysconfdir}/service
mkdir -p %{buildroot}%{_localstatedir}/service

%files
%defattr (-,root,root)
%{_bindir}/
%{_sysconfdir}/service
%{_localstatedir}/service
%{_libdir}/libftrigr.a
%{_libdir}/libftrigw.a
%{_libdir}/libs6.a

%changelog
* Thu Mar 14 2013 David Arroyo <droyo@aqwari.us> - 1.0.0-1
- Initial build
