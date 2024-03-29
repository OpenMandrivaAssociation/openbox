%define major 32
%define obtmajor 2
%define libobrender	%mklibname obrender
%define libobt		%mklibname obt
%define oldlibobrender	%mklibname obrender 32
%define oldlibobt		%mklibname obt 2
%define devname %mklibname -d %{name}

Summary:	Windowmanager based on the original blackbox-code
Name:		openbox
Version:	3.6.1
Release:	11
Group:		Graphical desktop/Other
License:	BSD
Url:		http://openbox.org/
Source0:	http://openbox.org/dist/openbox/%{name}-%{version}.tar.xz
# oxygen-theme here:
# http://box-look.org/content/show.php?content=145240
Source1:	http://box-look.org/CONTENT/content-files/145240-Oxynew.obt
# (tpg) breeze theme
#http://box-look.org/content/show.php/Mistral+%28Updated%29?content=167604
Source2:	mistral_openbox_by_phobi4n-d8ztvoc.tar.xz
Patch0:		openbox-3.5.2-unused-libs.patch
Patch1:		openbox-3.6.1-default-apps.patch
Patch100:	openbox-3.5.0-openmandriva_customisation.patch
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pangoxft)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(imlib2)
BuildRequires:	pkgconfig(sm)
Requires:	xsetroot
Suggests:	obconf-qt

%description
Openbox is a window manager for the X11 windowing system.
It currently runs on a large list of platforms. It was originally
based on blackbox and currently remains very similar, even using
blackbox styles (with available extensions) for its themeing.

Openbox is the spawn of a number of previous blackbox users/hackers.
Being overall pleased with the window manager, but feeling left unable
to contribute, this project was born.The Openbox project is developed,
maintained, and contributed to by these individuals.

%files -f %{name}.lang
%license CHANGELOG
%doc AUTHORS README
%doc %{_docdir}/openbox/*
%{_bindir}/obxprop
%{_bindir}/%{name}
%{_bindir}/openbox-session
%{_bindir}/startopenbox
%dir %{_sysconfdir}/xdg/%{name}
%config(noreplace) %{_sysconfdir}/xdg/%{name}/*
%{_libexecdir}/openbox-autostart
%{_libexecdir}/openbox-xdg-autostart
%{_mandir}/man1/obxprop.1.*
%{_mandir}/man1/openbox.1.*
%{_mandir}/man1/openbox-session.1.*
%{_datadir}/xsessions/openbox.desktop
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_datadir}/themes/*

#---------------------------------------------------------------------------

%package kde
Summary:	KDE support for %{name}
Group:		Graphical desktop/KDE
Requires:	%{name} = %{EVRD}

%description kde
KDE session support for %{name}.

%files kde
%{_bindir}/openbox-kde-session
%{_datadir}/xsessions/openbox-kde.desktop
%{_mandir}/man1/openbox-kde-session.1.*

#---------------------------------------------------------------------------

%package gnome
Summary:	GNOME support for %{name}
Group:		Graphical desktop/GNOME
Requires:	%{name} = %{EVRD}

%description gnome
GNOME session support for %{name}.

%files gnome
%{_bindir}/gdm-control
%{_bindir}/gnome-panel-control
%{_bindir}/openbox-gnome-session
%{_datadir}/xsessions/openbox-gnome.desktop
%{_datadir}/gnome-session/sessions/openbox-*.session
%{_datadir}/gnome/wm-properties/openbox.desktop
%{_mandir}/man1/openbox-gnome-session.1.*

#---------------------------------------------------------------------------

%package -n %{libobrender}
Summary:	Libraries from openbox
Group:		System/Libraries
Obsoletes:	%{_lib}openbox27 < 3.5.0-8
Obsoletes:	%{_lib}openbox29 < 3.6.1-1
Obsoletes:	%oldlibobrender < %{EVRD}

%description -n %{libobrender}
This package contains a shared library for %{name}.

%files -n %{libobrender}
%{_libdir}/libobrender.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{libobt}
Summary:	Libraries from openbox
Group:		System/Libraries
Conflicts:	%{_lib}openbox27 < 3.5.0-8
Obsoletes:	%oldlibobt < %{EVRD}

%description -n %{libobt}
This package contains a shared library for %{name}.

%files -n %{libobt}
%{_libdir}/libobt.so.%{obtmajor}*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files from openbox
Group:		Development/Other
Requires:	%{libobrender} = %{version}-%{release}
Requires:	%{libobt} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%files -n %{devname}
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/%{name}

#---------------------------------------------------------------------------

%prep
%setup -q -a1 -a2
%autopatch -p1
autoreconf -fi
2to3 -w data/autostart/openbox-xdg-autostart tools/themeupdate/themeupdate.py

%build
%configure
%make_build \
	DEFAULT_MENU=%{_sysconfdir}/xdg/openbox/menu.xml

%install
%make_install

# (tpg) Oxygen theme
mkdir -p %{buildroot}%{_datadir}/themes/oxygen/openbox-3/
install -m 0644 Oxynew/openbox-3/*.xbm Oxynew/openbox-3/themerc %{buildroot}%{_datadir}/themes/oxygen/openbox-3/

# (tpg) Mistral theme
mkdir -p %{buildroot}%{_datadir}/themes/Mistral/openbox-3/
install -m 0644 Mistral/openbox-3/*.xbm Mistral/openbox-3/themerc %{buildroot}%{_datadir}/themes/Mistral/openbox-3/

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/start%{name} <<EOF
#!/bin/sh
%{_bindir}/xsetroot -solid Black
exec %{_bindir}/openbox-session
EOF

# insall docs manually
rm -fr %{buildroot}%{_docdir}/%{name}/{AUTHORS,README}
# locales
%find_lang %{name}

