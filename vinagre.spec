Summary:	VNC client for the GNOME desktop
Summary(pl.UTF-8):	Klient VNC dla środowiska GNOME
Name:		vinagre
Version:	2.30.3
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/vinagre/2.30/%{name}-%{version}.tar.bz2
# Source0-md5:	adfa70f0fab9171d01f4c4cd4ede9e90
URL:		http://www.gnome.org/projects/vinagre/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.10
BuildRequires:	avahi-devel >= 0.6.22
BuildRequires:	avahi-glib-devel >= 0.6.22
BuildRequires:	avahi-gobject-devel >= 0.6.22
BuildRequires:	avahi-ui-devel >= 0.6.22
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd43-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gnome-panel-devel >= 2.24.0
BuildRequires:	gtk+2-devel >= 2:2.18.0
BuildRequires:	gtk-vnc-devel >= 0.3.10
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libgnome-keyring-devel >= 2.24.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	telepathy-glib-devel >= 0.7.31
BuildRequires:	vte-devel >= 0.20.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires(post,preun):	GConf2
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

%{__sed} -i -e 's/en@shaw//' po/LINGUAS
rm -f po/en@shaw.po

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-avahi=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

rm -f $RPM_BUILD_ROOT%{_libdir}/vinagre-1/{plugin-loaders,plugins}/*.la

# Remove text files installed by vinagre, we install them in a versioned
# directory in the files section
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/vinagre

%find_lang vinagre --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install vinagre.schemas
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall vinagre.schemas

%postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor

%files -f vinagre.lang
%defattr(644,root,root,755)
%doc README NEWS COPYING AUTHORS
%attr(755,root,root) %{_bindir}/vinagre
%dir %{_libdir}/vinagre-1
%dir %{_libdir}/vinagre-1/plugin-loaders
%attr(755,root,root) %{_libdir}/vinagre-1/plugin-loaders/libcloader.so
%dir %{_libdir}/vinagre-1/plugins
%attr(755,root,root) %{_libdir}/vinagre-1/plugins/libvnc.so
%{_libdir}/vinagre-1/plugins/vnc.vinagre-plugin
%attr(755,root,root) %{_libexecdir}/vinagre-applet
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_desktopdir}/*.desktop
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Vinagre.service
%{_datadir}/mime/packages/*.xml
%{_datadir}/telepathy/clients/Vinagre.client
%{_datadir}/vinagre
%{_datadir}/vinagre-1
%{_sysconfdir}/gconf/schemas/vinagre.schemas
%{_mandir}/man1/*.1*
%{_libdir}/bonobo/servers/GNOME_VinagreApplet.server

%files devel
%defattr(644,root,root,755)
%{_includedir}/vinagre-1.0
%{_pkgconfigdir}/vinagre-1.0.pc
