Summary:	VNC client for the GNOME desktop
Name:		vinagre
Version:	0.4
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://download.gnome.org/sources/vinagre/0.4/%{name}-%{version}.tar.bz2
# Source0-md5:	97dee0faa1b78e2497b9d231053b2f6d
URL:		http://www.gnome.org/projects/vinagre/
BuildRequires:	GConf2-devel >= 2.16.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	avahi-devel >= 0.6.18
BuildRequires:	avahi-glib-devel >= 0.6.18
BuildRequires:	avahi-ui-devel >= 0.6.18
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-keyring-devel
BuildRequires:	gtk+2-devel >= 2.11.6
BuildRequires:	gtk-vnc-devel >= 0.3.0
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 2.6.0
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Vinagre is a VNC client for the GNOME desktop environment.

%prep
%setup -q

%build
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-avahi=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# Remove text files installed by vinagre, we install them in a versioned
# directory in the files section
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/vinagre/

desktop-file-install 						\
	--remove-category=Application				\
	--add-category=GTK					\
	--delete-original					\
        --dir=$RPM_BUILD_ROOT%{_desktopdir}		\
        $RPM_BUILD_ROOT%{_desktopdir}/vinagre.desktop

%find_lang vinagre --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor

%files -f vinagre.lang
%defattr(644,root,root,755)
%doc README NEWS COPYING AUTHORS
%attr(755,root,root) %{_bindir}/*
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_desktopdir}/*.desktop
%{_datadir}/mime/packages/*.xml
%{_datadir}/%{name}/
