%define name		xmlrpc-c
%define version		1.06.27
%define release		%mkrel 5

%define	major		3
%define libname		%mklibname %name %major
%define develname	%mklibname -d %name

Name:		%name
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Version:	%version
Release:	%release
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
URL:		http://xmlrpc-c.sourceforge.net/
License:	BSD like
Group:		System/Libraries
Source:		xmlrpc-%{version}.tgz
Patch1:		%{name}_fpic.patch
Patch2:		xmlrpc-c-1.06.27-curl-easy-setopt.patch
Patch3:		xmlrpc-c-1.06.09-asneeded.patch
Patch4:		xmlrpc-c-1.06.27-abyss-header-fixup.patch
Patch5:		xmlrpc-c-1.06.27-gcc43-test-fix.patch
BuildRequires:	curl-devel libxml2-devel
Conflicts:	%mklibname %name

%description
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.


%package -n %{libname}
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Group:		System/Libraries
Obsoletes:	%mklibname %name

%package -n %{develname}
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Group:		System/Libraries
Requires:	%{libname} = %version-%release
Requires:	libxml2-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Conflicts:	%name < 1.06.27-2
Conflicts:	%mklibname %name

%description -n %{libname}
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

%description -n %{develname}
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

This package contains the devlopement files.

%prep
%setup -q 
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

aclocal --force
libtoolize --force
autoconf

sed -i -e "/CFLAGS_COMMON/s:-g -O3$:%{optflags}:" Makefile.common
sed -i -e "/CXXFLAGS_COMMON/s:-g$:%{optflags}:" Makefile.common

%build
%configure2_5x \
	--disable-wininet-client --enable-libxml2-backend \
	--disable-libwww-client --enable-curl-client
make

%clean
%{__rm} -Rf %{buildroot}

%install
rm -fr %buildroot
%makeinstall_std

%files
%defattr(-,root,root)
%doc doc/COPYING doc/CREDITS doc/DEVELOPING doc/HISTORY doc/SECURITY doc/TESTING doc/TODO
%{_bindir}/xmlrpc
%{_bindir}/xmlrpc_transport

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_bindir}/xmlrpc-c-config
%{_includedir}/*.h
%{_includedir}/%name
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so

