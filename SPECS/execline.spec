Name:         execline
Version:      1.2.0
Release:      2
License:      ISC
Source0:      http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz
Source1:      execline.eb
Source2:      execlineb.eb
Summary:      Minimal scripting language
Group:        Development/Languages
BuildRequires: /usr/bin/musl-gcc skalibs

%description
Execline is a small, secure scripting language.

%prep
%setup -q -n admin/%{name}-%{version}

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
echo %{_includedir}/skalibs     > path-include
echo %{_libdir}/skalibs         > path-library
echo /%{_lib}                   > path-library.so
echo %{_libdir}/skalibs/sysdeps > import
echo %{_libexecdir}/execline    > conf-install-command
echo %{_libdir}                 > conf-install-library
echo %{_includedir}             > conf-install-include
echo /%{_lib}                   > conf-install-library.so
echo %{_sysconfdir}             > conf-install-etc
popd

package/compile

%install

mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{_sourcedir}/execline.eb \
	%{buildroot}%{_bindir}/execline
install -m 0755 %{_sourcedir}/execlineb.eb \
	%{buildroot}%{_bindir}/execlineb
sed -i 's;__EXECLINEDIR__;%{_libexecdir}/execline;g' \
	%{buildroot}%{_bindir}/{execline,execlineb}

for i in package/*.exported 
do 
	case ${i##*/} in
	library.so.exported) d=/%{_lib}                ;;
	include.exported)    d=%{_includedir}          ;;
	library.exported)    d=%{_libdir}              ;;
	command.exported)    d=%{_libexecdir}/execline ;;
	esac
	mkdir -p %{buildroot}$d
	f=`basename $i|sed 's/.exported//'`
	cp `sed s,^,$f/, $i` %{buildroot}${d}/
done

%files
%defattr (-,root,root)
%{_libexecdir}/execline/
%{_libdir}/*.a
%{_includedir}/*.h
/%{_lib}/*.so
%{_bindir}/execline
%{_bindir}/execlineb

%changelog
* Fri Mar 15 2013 David Arroyo <droyo@aqwari.us> - 1.0.0-2
- Update to fix hardcoded path issues

* Thu Mar 14 2013 David Arroyo <droyo@aqwari.us> - 1.2.0-1
- Initial build
