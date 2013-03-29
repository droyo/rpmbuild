Name:         musl
Summary:      A lightweight standard C library
Version:      0.9.9
Release:      2
License:      MIT
Group:        Development/Libraries
Source:       http://www.musl-libc.org/releases/%{name}-%{version}.tar.gz

%description
musl is a “libc”, an implementation of the standard library functionality
described in the ISO C and POSIX standards, plus common extensions,
intended for use on Linux-based systems.

%prep
%setup -q

%build
rm -rf %{buildroot}
%configure \
	--libdir=%{_libdir}/musl \
	--includedir=%{_includedir}/musl \
	--bindir=%{_bindir} \
	--syslibdir=/%{_lib}

make

%install
make DESTDIR=%{buildroot} install

%files
%defattr (-,root,root)
/%{_lib}/ld-musl-%{_arch}.so.1
%{_bindir}/musl-gcc
%{_libdir}/
%{_includedir}/

%changelog
* Thu Mar 28 2013 David Arroyo <droyo@aqwari.us> - 0.9.9-2
- Remove conflict with glibc

* Tue Mar 12 2013 David Arroyo <droyo@aqwari.us> - 0.9.9-1
- Initial build
