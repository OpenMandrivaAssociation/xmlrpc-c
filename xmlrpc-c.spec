%define	major		3
%define libname		%mklibname %name %major
%define develname	%mklibname -d %name

%global                 advanced_branch		1
%global                 svnrev			2233

Name:		xmlrpc-c
Summary:	Programming library for writing an XML-RPC server or client in C or C++
Version:	1.29.0
Release:	4
License:	BSD like
Group:		System/Libraries
URL:		http://xmlrpc-c.sourceforge.net/
%{!?advanced_branch:Source0:	http://dl.sourceforge.net/sourceforge/xmlrpc-c/xmlrpc-%version.tgz}
# generated by 'make svn-sources [SVN_VER=%version SVN_REV=%svnrev]'. Unfortunately,
# upstream does not tag versions so we must fetch from the branch and
# check which version was used for it
%{?advanced_branch:Source0:	xmlrpc-c-%version.tar.xz}
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
Summary:        Programming library for writing an XML-RPC server or client in C or C++
Group:          System/Libraries
Requires:       %{libname} = %version-%release
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
%setup -q 
%apply_patches

%build
%cmake \
    -D_lib:STRING=%_lib \
    -DMUST_BUILD_CURL_CLIENT:BOOL=ON \
    -DMUST_BUILD_LIBWWW_CLIENT:BOOL=OFF \
    -DENABLE_TOOLS:BOOL=ON

%__cxx $RPM_OPT_FLAGS %SOURCE100 -o depsort

%make

%install
cd build
%makeinstall_std

bash %SOURCE101 "$RPM_BUILD_ROOT" "%_libdir" 'libxmlrpc' $RPM_BUILD_ROOT%_libdir/libxmlrpc*.so.[0-9]

%check
unset PKG_CONFIG_PATH
export PKG_CONFIG_LIBDIR=$RPM_BUILD_ROOT%_libdir/pkgconfig:%_libdir/pkgconfig:%_datadir/pkgconfig
PATH=$RPM_BUILD_ROOT%_bindir:$PATH

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



%changelog

* Mon Jan 16 2012 dmorgan <dmorgan> 1.29.0-1.mga2
+ Revision: 196758
- New version 1.29.0
  Sync patches with fedora

* Sun May 15 2011 pterjan <pterjan> 1.20.3-5.mga1
+ Revision: 99045
- Rebuild for fixed find-requires

* Wed Apr 27 2011 dmorgan <dmorgan> 1.20.3-4.mga1
+ Revision: 92205
- Rebuild because of missing package in i586

  + pterjan <pterjan>
    - Drop old conflicts/obsoletes
    - imported package xmlrpc-c


* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.20.3-3mdv2011.0
+ Revision: 608224
- rebuild

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - rebuild for ncurse support

* Sun Nov 29 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.20.3-1mdv2010.1
+ Revision: 471450
- fix lib64 build
- take upstream version from subversion, as there is no tarball release
  available
- sync with fedora package

* Thu Jan 22 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.06.27-5mdv2009.1
+ Revision: 332399
- don't modify Makefile.common for setting %%{optflags}, override the variables by
  passing them to 'make', also compile with -O3 which is suggsted by the default
  compile flags
- ensure that libtool and friends gets updated, otherwise ancient libtool will
  be used, resulting in inability to link against correct libraries, thus leaving
  the build completely broken

* Wed Jan 21 2009 Helio Chissini de Castro <helio@mandriva.com> 1.06.27-4mdv2009.1
+ Revision: 332216
- Rraise release to recompile and solve xml2 linking issues in the library

* Sun Sep 07 2008 Gaëtan Lehmann <glehmann@mandriva.org> 1.06.27-3mdv2009.0
+ Revision: 282075
- * rebuild for new libxml2
  * devel package requires libxml2-devel

* Sun Jul 13 2008 Funda Wang <fwang@mandriva.org> 1.06.27-2mdv2009.0
+ Revision: 234252
- move xmlrpc-c-config into devel package

* Sun Jul 13 2008 Funda Wang <fwang@mandriva.org> 1.06.27-1mdv2009.0
+ Revision: 234251
- BR xml2
- fix typo of develname
- use own optflags
- New version 1.06.27
- merge gentoo patches

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Nicolas Vigier <nvigier@mandriva.com>
    - add Provides on libxmlrpc-c-devel

* Wed May 23 2007 Nicolas Vigier <nvigier@mandriva.com> 1.06.14-1mdv2008.0
+ Revision: 30032
- Update to version 1.06.14

* Wed May 09 2007 Nicolas Vigier <nvigier@mandriva.com> 1.06.13-1mdv2008.0
+ Revision: 25644
- Import xmlrpc-c

