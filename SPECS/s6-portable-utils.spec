Name:         s6-portable-utils
Version:      1.0.0
Release:      2
License:      ISC
Source:       http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Summary:      Tiny Linux-specific utilities
Group:        System Environment/Base
BuildRequires: /usr/bin/musl-gcc skalibs

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
echo %{_includedir}/skalibs     > path-include
echo %{_libdir}/skalibs         > path-library
echo /%{_lib}                   > path-library.so
echo %{_libdir}/skalibs/sysdeps > import
echo %{_bindir}                 > conf-install-command
echo %{_libdir}                 > conf-install-library
echo %{_includedir}             > conf-install-include
echo /%{_lib}                   > conf-install-library.so
echo %{_sysconfdir}             > conf-install-etc

popd
package/compile

%install

for i in package/*.exported 
do 
	case ${i##*/} in
	library.so.exported) d=/%{_lib}       ;;
	include.exported)    d=%{_includedir} ;;
	library.exported)    d=%{_libdir}     ;;
	command.exported)    d=%{_bindir}     ;;
	esac
	mkdir -p %{buildroot}$d
	f=`basename $i|sed 's/.exported//'`
	install `sed s,^,$f/, $i` %{buildroot}$d
done

%files
%defattr (-,root,root)
%{_bindir}/

%changelog
* Fri Mar 15 2013 David Arroyo <droyo@aqwari.us> - 1.0.0-2
- Update to fix hardcoded path issues

* Thu Mar 14 2013 David Arroyo <droyo@aqwari.us> - 1.0.0-1
- Initial build
