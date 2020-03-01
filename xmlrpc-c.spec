%define	major		3
%define libname		%mklibname %name %major
%define develname	%mklibname %name -d

#define advanced_branch	1

# Upstream libxml2 backend is completely broken since 2015
# https://sourceforge.net/p/xmlrpc-c/patches/49/
%bcond_with libxml2

Name:		xmlrpc-c
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Version:	1.51.05
Release:	%mkrel 2
Group:		System/Libraries
# See doc/COPYING for details.
# The Python 1.5.2 license used by a few files is just BSD.
License:        BSD and MIT
URL:            http://xmlrpc-c.sourceforge.net/
%{!?advanced_branch:Source0: https://downloads.sourceforge.net/xmlrpc-c/xmlrpc-c-%version.tgz}
# generated by 'make svn-sources [SVN_VER=version SVN_REV=rev]'. Unfortunately,
# upstream does not tag versions so we must fetch from the branch and
# check which version was used for it
%{?advanced_branch:Source0: xmlrpc-c-%version.tar.xz}

# Upstreamable patches
Patch101:       0001-xmlrpc_server_abyss-use-va_args-properly.patch
Patch102:       0002-Use-proper-datatypes-for-long-long.patch
Patch103:       0003-allow-30x-redirections.patch
#Patch104:       xmlrpc-c-printf-size_t.patch
#Patch105:       xmlrpc-c-check-vasprintf-return-value.patch

# Meson buildsystem, see https://blogs.gnome.org/ignatenko/2016/12/17/meson-%E2%99%A5-xmlrpc-c/
Patch1001:      0001-add-meson-buildsystem-definitions.patch
Patch1002:      0002-chmod-x-xml-rpc-api2txt.patch

BuildRequires:  git-core
BuildRequires:  meson >= 0.36.0
%if %{with libxml2}
BuildRequires:  pkgconfig(libxml-2.0)
%endif
BuildRequires:  pkgconfig(openssl) >= 1.1
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(readline)
BuildRequires:  ncurses-devel

%description
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

%files
%doc doc/COPYING doc/CREDITS doc/DEVELOPING
%doc doc/HISTORY doc/SECURITY doc/TESTING doc/TODO
%{_bindir}/xmlrpc
%{_bindir}/xmlrpc_dumpserver
%{_bindir}/xmlrpc_parsecall
%{_bindir}/xmlrpc_pstream
%{_bindir}/xmlrpc_transport
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
Summary:        Programming library for writing an XML-RPC server or client in C or C++
Group:          System/Libraries
Requires:       %{libname} = %version-%release
Requires:       %{name} >= %version
Requires:       libxml2-devel
Provides:       %{name}-devel = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
XML-RPC is a quick-and-easy way to make procedure calls over the Internet.
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML.

This library provides a modular implementation of XML-RPC for C and C++.

This package contains the developement files.

%files -n %{develname}
%{_bindir}/xmlrpc-c-config
%{_includedir}/*.h
%{_includedir}/%name
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

#--------------------------------------------------------------------

%prep
%autosetup -Sgit

%build
%meson %{?with_libxml2:-Dlibxml2-backend=true}
%meson_build

%install
%meson_install

%check
unset PKG_CONFIG_PATH
export PKG_CONFIG_LIBDIR=%buildroot%_libdir/pkgconfig:%_libdir/pkgconfig:%_datadir/pkgconfig
PATH=%buildroot%_bindir:$PATH

_e() {
     echo "\$ $@"
     "$@"
}

set +x
_e xmlrpc-c-config --help
for comp in cgi-server server-util abyss-server client libwww-client; do
	for opt in '--version' '--libs'; do
		_e xmlrpc-c-config "$comp" $opt
	done
done
set -x
