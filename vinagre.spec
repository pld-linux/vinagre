Summary:	VNC client for the GNOME desktop
Summary(pl.UTF-8):	Klient VNC dla środowiska GNOME
Name:		vinagre
Version:	2.91.91
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/vinagre/2.91/%{name}-%{version}.tar.bz2
# Source0-md5:	3c776450c2cb89ded68664edeaf4f0e0
URL:		http://www.gnome.org/projects/vinagre/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.10
BuildRequires:	avahi-gobject-devel >= 0.6.26
BuildRequires:	avahi-ui-gtk3-devel >= 0.6.26
BuildRequires:	docbook-dtd43-xml
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils >= 0.14.0
# applet broken for now
#BuildRequires:	gnome-panel-devel >= 2.91.91
BuildRequires:	gobject-introspection-devel >= 0.9.3
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk3-vnc-devel >= 0.4.3
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libgnome-keyring-devel >= 2.24.0
BuildRequires:	libpeas-devel >= 0.7.2
BuildRequires:	libpeas-gtk-devel >= 0.7.2
BuildRequires:	libtool >= 2.2.6
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig >= 0.16
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
#BuildRequires:	spice-slient-gtk-3.0 >= 0.5
BuildRequires:	telepathy-glib-devel >= 0.11.6
BuildRequires:	vte-devel >= 0.20.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
# for im status plugin
Requires:	libpeas-loader-seed >= 0.7.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Vinagre is a VNC client for the GNOME desktop environment.

%description -l pl.UTF-8
Vinagre to klient VNC dla środowiska graficznego GNOME.

%package devel
Summary:	Header files for vinagre
Summary(pl.UTF-8):	Pliki nagłówkowe dla vinagre
Group:		Development/Libraries
Requires:	gtk+2-devel >= 2:2.18.0
Requires:	libxml2-devel >= 1:2.6.31

%description devel
Header files for vinagre.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla vinagre.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-avahi \
	--with-telepathy \
	--without-panelapplet \
	--enable-introspection \
	--disable-spice \
	--disable-silent-rules \
	--disable-scrollkeeper \
	--disable-schemas-compile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/vinagre-1/{plugin-loaders,plugins}/*.la

# Remove text files installed by vinagre, we install them in a versioned
# directory in the files section
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/vinagre

%find_lang vinagre --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor

%files -f vinagre.lang
%defattr(644,root,root,755)
%doc README NEWS COPYING AUTHORS
%attr(755,root,root) %{_bindir}/vinagre
%dir %{_libdir}/vinagre-1
%dir %{_libdir}/vinagre-1/girepository-1.0
%{_libdir}/vinagre-1/girepository-1.0/Vinagre-3.0.typelib
%dir %{_libdir}/vinagre-1/plugins
%attr(755,root,root) %{_libdir}/vinagre-1/plugins/libvnc.so
%attr(755,root,root) %{_libdir}/vinagre-1/plugins/libreversevnc.so
%{_libdir}/vinagre-1/plugins/vnc.plugin
%{_libdir}/vinagre-1/plugins/im-status.plugin
%{_libdir}/vinagre-1/plugins/reverse-vnc.plugin
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_desktopdir}/*.desktop
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Vinagre.service
%{_datadir}/glib-2.0/schemas/org.gnome.Vinagre.gschema.xml
%{_datadir}/mime/packages/*.xml
%{_datadir}/telepathy/clients/Vinagre.client
%{_datadir}/vinagre
%{_datadir}/vinagre-1
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/vinagre-1.0
%{_pkgconfigdir}/vinagre-1.0.pc
