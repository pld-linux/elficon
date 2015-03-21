#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#
Summary:	Adding icons to ELF binaries
Name:		elficon
Version:	0.6.0
Release:	0.2
# libr: LGPL v2.1; libr-libbfd backend: LGPL v3; elfres, gnome-thumbnailer: MIT
License:	LGPL v2.1, LGPL v3, MIT
Group:		Applications
Source0:	http://www.compholio.com/elfres/download.php?file=%{name}_%{version}.tar.gz
# Source0-md5:	6ad0ff2dbd9f561b7372a03b5d82c778
Patch0:		libtool.patch
Patch1:		default-icon.patch
URL:		http://www.compholio.com/elfres/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project is intended to provide an easy to use mechanism for
managing (embedding, retrieving, deleting) resources in ELF binaries.
The project has two components: elfres and libr. elfres is a resource
editor and an example of how to utilize the libr library. The libr
library provides a solid API and ABI that implements the preliminary
spec for adding ELF resources (icons or otherwise) documented at:
<https://wiki.ubuntu.com/ELFIconSpec>

%package -n libr
Summary:	Library to manage resources in ELF binaries
# library: LGPL v2.1, backend for libbfd: LGPL v3
License:	LGPL v2.1, LGPL v3
Group:		Libraries

%description -n libr
This library is intended to provide an easy to use mechanism for
managing (embedding, retrieving, deleting) resources in ELF binaries.

%package -n libr-devel
Summary:	Header files for libr library
Group:		Development/Libraries
Group:		Libraries
Requires:	libr = %{version}-%{release}

%description -n libr-devel
Header files for libr library.

%package -n elfres
Summary:	elfres - Manage application resources in ELF binaries
License:	MIT
Group:		Applications
Requires:	libr = %{version}-%{release}

%description -n elfres
This application is a technology demonstration, at this point please
DO NOT consider this implementation to be a specification for how ELF
icons will be supported by desktop environments. With that said, this
application and the associated "libr" resource library provide a solid
mechanism for managing application resources that you are free to use
in your own applications.

%package -n gnome-elf-thumbnailer
Summary:	Generate thumbnailers for ELF binaries with icons
License:	MIT
Group:		X11/Applications
Requires:	elfres = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
Requires:	gnome-themes-standard

%description -n gnome-elf-thumbnailer
Generate thumbnailers for ELF binaries with icons.

%prep
%setup -qc
%patch0 -p1
%patch1 -p1

%build

# libr
cd libr
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
%if "%{?configure_cache}" == "1"
	--cache-file=%{?configure_cache_file}%{!?configure_cache_file:configure}-libr.cache
%endif
%{__make}

export PKG_CONFIG_PATH=$(pwd)
export CPPFLAGS="%{rpmcppflags} -I$(pwd)/src"
export LDFLAGS="%{rpmldflags} -L$(pwd)/src/.libs"

# elfres
cd ../elfres
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
%if "%{?configure_cache}" == "1"
	--cache-file=%{?configure_cache_file}%{!?configure_cache_file:configure}-elfres.cache
%endif
%{__make}

# gnome-elf-thumbnailer
# nothing to build

%install
rm -rf $RPM_BUILD_ROOT
# libr
%{__make} -C libr install \
	FAKEROOTKEY=1 \
	DESTDIR=$RPM_BUILD_ROOT
# obsoleted by pkgconfig file
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libr.la

# elfres
%{__make} -C elfres install \
	DESTDIR=$RPM_BUILD_ROOT
ln -s elfres $RPM_BUILD_ROOT%{_bindir}/elficon

# gnome-elf-thumbnailer
install -d $RPM_BUILD_ROOT%{_datadir}/gconf/schemas
%{__make} -C gnome-elf-thumbnailer install \
	DESTDIR=$RPM_BUILD_ROOT
install -p gnome-elf-thumbnailer/src/gnome-elf-thumbnailer.sh $RPM_BUILD_ROOT%{_bindir}

%find_lang elfres

%post	-n libr -p /sbin/ldconfig
%postun	-n libr -p /sbin/ldconfig

%post -n gnome-elf-thumbnailer
%glib_compile_schemas

%postun -n gnome-elf-thumbnailer
%glib_compile_schemas

%clean
rm -rf $RPM_BUILD_ROOT

%files -n libr
%defattr(644,root,root,755)
%doc libr/{AUTHORS,ChangeLog}
%{_libdir}/libr.so.*.*.*
%ghost %{_libdir}/libr.so.0

%files -n libr-devel
%defattr(644,root,root,755)
%{_includedir}/libr
%{_libdir}/libr.so
%{_pkgconfigdir}/libr.pc
%{_mandir}/man3/IconSVG.3*
%{_mandir}/man3/OneCanvasIconInfo.3*
%{_mandir}/man3/libr_*.3*

%files -n elfres -f elfres.lang
%defattr(644,root,root,755)
%doc elfres/{AUTHORS,COPYING,ChangeLog,README}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/elficon
%attr(755,root,root) %{_bindir}/elfres

%files -n gnome-elf-thumbnailer
%defattr(644,root,root,755)
%doc gnome-elf-thumbnailer/{COPYING,README}
%attr(755,root,root) %{_bindir}/gnome-elf-thumbnailer.sh
%{_datadir}/gconf/schemas/gnome-elf-thumbnailer.schemas
