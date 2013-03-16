Name:         skalibs
Version:      1.3.0
Release:      2
License:      ISC
Source:       http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Summary:      General-purpose development libraries
Group:        Development/Libraries
BuildRequires: /usr/bin/musl-gcc

%description
skalibs is a package centralizing the free software / open source C development
files used for building all software at skarnet.org: it contains essentially
general-purpose libraries.

%prep
%setup -q -n prog/%{name}-%{version}

%build
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}%{_libdir}
pushd conf-compile

rm -f flag-slashpackage
echo 'musl-gcc'                 > conf-cc
echo 'musl-gcc -static'         > conf-ld
echo 'musl-gcc'                 > conf-dynld
echo %{_sysconfdir}             > conf-etc
echo %{_bindir}                 > conf-install-command
echo %{_includedir}/skalibs     > conf-install-include
echo %{_libdir}/skalibs         > conf-install-library
echo /%{_lib}                   > conf-install-library.so
echo %{_libdir}/skalibs/sysdeps > conf-install-sysdeps

popd
package/compile

%install

for i in package/*.exported 
do 
	case ${i##*/} in
	library.so.exported) d=/%{_lib}                   ;;
	include.exported)    d=%{_includedir}/skalibs     ;;
	sysdeps.exported)    d=%{_libdir}/skalibs/sysdeps ;;
	library.exported)    d=%{_libdir}/skalibs         ;;
	command.exported)    d=%{_bindir}                 ;;
	esac
	mkdir -p %{buildroot}$d
	f=`basename $i|sed 's/.exported//'`
	install `sed s,^,$f/, $i` %{buildroot}$d
done
mkdir -p %{buildroot}%{_sysconfdir}
install etc/leapsecs.dat %{buildroot}%{_sysconfdir}

%files
%defattr (-,root,root)
%{_includedir}/skalibs/
%{_libdir}/skalibs/
%{_sysconfdir}/leapsecs.dat
/%{_lib}/*.so

%changelog
* Fri Mar 15 2013 David Arroyo <droyo@aqwari.us> - 1.0.0-2
- Update to fix hardcoded path issues

* Thu Mar 14 2013 David Arroyo <droyo@aqwari.us> - 1.3.0-1
- Initial build
