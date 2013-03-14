Name:         execline
Version:      1.2.0
Release:      1
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
echo %{buildroot}%{_libexecdir}/execline    > conf-install-command
echo %{buildroot}%{_libdir}                 > conf-install-library
echo %{buildroot}%{_includedir}             > conf-install-include
echo %{buildroot}/%{_lib}                   > conf-install-library.so
echo %{buildroot}%{_sysconfdir}             > conf-install-etc

popd

make

%install

make install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{_sourcedir}/execline.eb \
	%{buildroot}%{_bindir}/execline
install -m 0755 %{_sourcedir}/execlineb.eb \
	%{buildroot}%{_bindir}/execlineb
sed -i 's;__EXECLINEDIR__;%{_libexecdir}/execline;g' \
	%{buildroot}%{_bindir}/{execline,execlineb}

%files
%defattr (-,root,root)
%{_libexecdir}/execline/
%{_libdir}/libexecline.a
%{_includedir}/execline.h
%{_includedir}/execline-config.h
%{_bindir}/execline
%{_bindir}/execlineb

%changelog
* Thu Mar 14 2013 David Arroyo <droyo@aqwari.us> - 1.2.0-1
- Initial build
