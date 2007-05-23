%define name		xmlrpc-c
%define version		1.06.14
%define release		%mkrel 1

%define libname_orig	xmlrpc-c
%define libname		%mklibname %{libname_orig}

Name:		%name
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Version:	%version
Release:	%release
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
URL:		http://xmlrpc-c.sourceforge.net/
License:	BSD like
Group:		System/Libraries
Source:		%{name}-%{version}.tgz
Patch0:		%{name}_wwwssl.patch
Patch1:		%{name}_fpic.patch
BuildRequires:	w3c-libwww-devel >= 5.3.2
BuildRequires:	curl-devel

%description
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.


%package -n %{libname}
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Group:		System/Libraries

%package -n %{libname}-devel
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Group:		System/Libraries
Requires:	%{libname}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

%description -n %{libname}-devel
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

This package contains the devlopement files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./configure \
  --bindir=%{_bindir} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir} \
  --with-libwww-ssl

perl -pi -e 's|(LIBWWW_LDADD@,-L/usr/lib\S*)|$1 -lwwwssl|' config.status
./config.status
chmod +x xmlrpc-c-config.test
%make

%clean
%{__rm} -Rf %RPM_BUILD_ROOT
%{__rm} -Rf %{buildroot}

%install
%makeinstall DESTDIR=$RPM_BUILD_ROOT

%files -n %{libname}
%defattr(-,root,root)
%doc doc/COPYING doc/CREDITS doc/DEVELOPING doc/HISTORY doc/SECURITY doc/TESTING doc/TODO
%{_bindir}/*
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so

