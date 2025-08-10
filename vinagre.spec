#
# Conditional build:
%bcond_with	rdp	# RDP support
%bcond_without	spice	# Spice support
%bcond_without	ssh	# SSH support

Summary:	VNC client for the GNOME desktop
Summary(pl.UTF-8):	Klient VNC dla środowiska GNOME
Name:		vinagre
Version:	3.22.0
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/vinagre/3.22/%{name}-%{version}.tar.xz
# Source0-md5:	451554ddf46636105cd5f0330e98d254
Patch0:		%{name}-freerdp.patch
Patch1:		c99.patch
URL:		https://wiki.gnome.org/Apps/Vinagre
BuildRequires:	appstream-glib-devel
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	avahi-gobject-devel >= 0.6.26
BuildRequires:	avahi-ui-gtk3-devel >= 0.6.26
BuildRequires:	dbus-glib-devel
%{?with_rdp:BuildRequires:	freerdp-devel >= 1.0}
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gtk+3-devel >= 3.9.6
BuildRequires:	gtk3-vnc-devel >= 0.4.3
BuildRequires:	intltool >= 0.50.0
BuildRequires:	itstool
BuildRequires:	libsecret-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig >= 1:0.24
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	spice-gtk-devel >= 0.5
BuildRequires:	tar >= 1:1.22
BuildRequires:	telepathy-glib-devel >= 0.12.0
BuildRequires:	vala >= 2:0.12.0
%{?with_ssh:BuildRequires:	vte-devel >= 0.28.0}
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.32.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	shared-mime-info
Requires:	glib2 >= 1:2.32.0
Requires:	gtk+3 >= 3.9.6
Requires:	gtk3-vnc >= 0.4.3
Requires:	hicolor-icon-theme
Requires:	libxml2 >= 1:2.6.31
%{?with_ssh:Requires:	vte >= 0.28.0}
Suggests:	openssh-clients
Obsoletes:	gnome-applet-vinagre
Obsoletes:	vinagre-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Vinagre is a VNC client for the GNOME desktop environment.

%description -l pl.UTF-8
Vinagre to klient VNC dla środowiska graficznego GNOME.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	SSH_PROGRAM=%{_bindir}/ssh \
	--with-avahi \
	--with-telepathy \
	%{!?with_rdp:--disable-rdp} \
	--disable-silent-rules \
	--disable-schemas-compile \
	%{!?with_spice:--disable-spice} \
	%{!?with_ssh:--disable-ssh}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang vinagre --with-gnome

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/vinagre
%{_datadir}/GConf/gsettings/org.gnome.Vinagre.convert
%{_datadir}/metainfo/vinagre.appdata.xml
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Vinagre.service
%{_datadir}/glib-2.0/schemas/org.gnome.Vinagre.gschema.xml
%{_datadir}/mime/packages/vinagre-mime.xml
%{_datadir}/telepathy/clients/Vinagre.client
%{_datadir}/vinagre
%{_desktopdir}/vinagre-file.desktop
%{_desktopdir}/vinagre.desktop
%{_iconsdir}/hicolor/*x*/mimetypes/application-x-remote-connection.png
%{_iconsdir}/hicolor/*x*/mimetypes/application-x-vnc.png
%{_iconsdir}/hicolor/*x*/status/view-minimize.png
%{_iconsdir}/hicolor/scalable/mimetypes/application-x-remote-connection.svg
%{_iconsdir}/hicolor/scalable/mimetypes/application-x-vnc.svg
%{_mandir}/man1/vinagre.1*
