%define name		xmlrpc-c
%define version		1.20.3
%define revision    1841
%define release		%mkrel 3

%define	major		3
%define libname		%mklibname %name %major
%define develname	%mklibname -d %name

Name:		%name
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Version:	%version
Release:	%release
License:	BSD like
Group:		System/Libraries
URL:		http://xmlrpc-c.sourceforge.net/
Source:		http://dl.sourceforge.net/sourceforge/xmlrpc-c/xmlrpc-c-%{version}.tar.bz2
Patch100: xmlrpc-c-cmake.patch 
Patch102: xmlrpc-c-printf-size_t.patch
Patch105: xmlrpc-c-longlong.patch
Patch106: xmlrpc-c-va_list.patch
Patch107: xmlrpc-c-uninit-curl.patch
Patch108: xmlrpc-c-verbose-curl.patch 
BuildRequires:	libxml2-devel
BuildRequires:	curl-devel
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel 
BuildRequires:	cmake
Conflicts:	%mklibname %name
BuildRoot:	%{_tmppath}/%{name}-%{version}

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
%setup -q -n %{name}
%patch100 -p1
%patch102 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1


%build
%cmake \
    -D_lib:STRING=%_lib \
    -DMUST_BUILD_CURL_CLIENT:BOOL=ON \
    -DMUST_BUILD_LIBWWW_CLIENT:BOOL=OFF \
    -DENABLE_TOOLS:BOOL=ON
%make

%clean
%{__rm} -Rf %{buildroot}

%install
rm -fr %buildroot
cd build
%makeinstall_std

%files
%defattr(-,root,root)
%doc doc/COPYING doc/CREDITS doc/DEVELOPING doc/HISTORY doc/SECURITY doc/TESTING doc/TODO
%{_bindir}/xmlrpc
%{_bindir}/xmlrpc_transport
%{_bindir}/xmlrpc_pstream
%{_bindir}/xml-rpc-api2cpp
%{_bindir}/xml-rpc-api2txt
%{_bindir}/xmlrpc_cpp_proxy
%{_mandir}/man1/xml-rpc-api2cpp.1*
%{_mandir}/man1/xml-rpc-api2txt.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_bindir}/xmlrpc-c-config
%{_includedir}/*.h
%{_includedir}/%name
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

