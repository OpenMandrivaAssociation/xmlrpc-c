%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

%global advanced_branch 1
%global svnrev 2233

Name:		xmlrpc-c
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Version:	1.51.06
Release:	1
License:	BSD like
Group:		System/Libraries
URL:		http://xmlrpc-c.sourceforge.net/
Source0:	https://downloads.sourceforge.net/xmlrpc-c/xmlrpc-c-%version.tgz
Source100:	dfs.cc
Source101:	dso-fixup
Patch100:	xmlrpc-c-cmake.patch
Patch102:	xmlrpc-c-printf-size_t.patch
Patch105:	xmlrpc-c-longlong.patch
Patch107:	xmlrpc-c-uninit-curl.patch
Patch108:	xmlrpc-c-30x-redirect.patch
Patch109:	xmlrpc-c-check-vasprintf-return-value.patch
Patch110:	xmlrpc-c-include-string_int.h.patch
BuildRequires:	libxml2-devel
BuildRequires:	curl-devel
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel 
BuildRequires:	cmake

%description
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

%files
%doc doc/COPYING doc/CREDITS doc/DEVELOPING doc/HISTORY doc/SECURITY doc/TESTING doc/TODO
%{_bindir}/xmlrpc
%{_bindir}/xmlrpc_transport
%{_bindir}/xmlrpc_pstream
%{_bindir}/xml-rpc-api2cpp
%{_bindir}/xml-rpc-api2txt
%{_bindir}/xmlrpc_cpp_proxy
%{_mandir}/man1/xml-rpc-api2cpp.1*
%{_mandir}/man1/xml-rpc-api2txt.1*

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Group:		System/Libraries

%description -n %{libname}
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

%files -n %{libname}
%{_libdir}/lib*.so.*

#--------------------------------------------------------------------

%package -n %{develname}
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
Requires:	libxml2-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

This package contains the developement files.

%files -n %{develname}
%{_bindir}/xmlrpc-c-config
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

#--------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
    -D_lib:STRING=%{_lib} \
    -DMUST_BUILD_CURL_CLIENT:BOOL=ON \
    -DMUST_BUILD_LIBWWW_CLIENT:BOOL=OFF \
    -DENABLE_TOOLS:BOOL=ON

%__cxx %{optflags} %SOURCE100 -o depsort

%make_build

%install
cd build
%make_install

bash %SOURCE101 "%{buildroot}" "%{_libdir}" 'libxmlrpc' %{buildroot}%{_libdir}/libxmlrpc*.so.[0-9]

%check
unset PKG_CONFIG_PATH
export PKG_CONFIG_LIBDIR=%{buildroot}%{_libdir}/pkgconfig:%{_libdir}/pkgconfig:%{_datadir}/pkgconfig
PATH=%{buildroot}%{_bindir}:$PATH

_e() {
     echo "\$ $@"
     "$@"
}

set +x
_e xmlrpc-c-config --help
for comp in c++ cgi-server server-util abyss-server client libwww-client; do
	for opt in '--version' '--libs' 'c++2 --libs' 'c++ --libs --static'; do
		_e xmlrpc-c-config "$comp" $opt
	done
done
set -x
