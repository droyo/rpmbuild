Name:         skalibs
Version:      1.3.0
Release:      1
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

touch flag-allstatic
rm -f flag-slashpackage
echo 'musl-gcc'                 > conf-cc
echo 'musl-gcc -static'         > conf-ld
echo 'musl-gcc'                 > conf-dynld
echo %{buildroot}%{_sysconfdir}             > conf-etc
echo %{buildroot}%{_bindir}                 > conf-install-command
echo %{buildroot}%{_includedir}/skalibs     > conf-install-include
echo %{buildroot}%{_libdir}/skalibs         > conf-install-library
echo %{buildroot}/%{_lib}                   > conf-install-library.so
echo %{buildroot}%{_libdir}/skalibs/sysdeps > conf-install-sysdeps

popd

%install

make install

%files
%defattr (-,root,root)
%{_includedir}/skalibs/
%{_libdir}/skalibs/
%{_sysconfdir}/leapsecs.dat

%changelog
* Thu Mar 14 2013 David Arroyo <droyo@aqwari.us> - 1.3.0-1
- Initial build
