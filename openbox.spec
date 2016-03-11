%define major 32
%define obtmajor 2
%define libobrender %mklibname obrender %{major}
%define libobt %mklibname obt %{obtmajor}
%define devname %mklibname -d %{name}

Summary:	Windowmanager based on the original blackbox-code
Name:		openbox
Version:	3.6.1
Release:	5
Group:		Graphical desktop/Other
License:	BSD
Url:		http://openbox.org/
Source0:	http://openbox.org/dist/openbox/%{name}-%{version}.tar.xz
Patch0:		openbox-3.5.0-mandriva_customisation.patch
Patch1:		openbox-3.5.2-unused-libs.patch
# oxygen-theme here:
# http://box-look.org/content/show.php?content=145240
Source1:	http://box-look.org/CONTENT/content-files/145240-Oxynew.obt
# (tpg) breeze theme
#http://box-look.org/content/show.php/Mistral+%28Updated%29?content=167604
Source2:	mistral_openbox_by_phobi4n-d8ztvoc.tar.xz
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
Suggests:	obconf

%description
Openbox is a window manager for the X11 windowing system.
It currently runs on a large list of platforms. It was originally
based on blackbox and currently remains very similar, even using
blackbox styles (with available extensions) for its themeing.

Openbox is the spawn of a number of previous blackbox users/hackers.
Being overall pleased with the window manager, but feeling left unable
to contribute, this project was born.The Openbox project is developed,
maintained, and contributed to by these individuals.

%package kde
Summary:	KDE support for %{name}
Group:		Graphical desktop/KDE
Requires:	%{name} = %{EVRD}

%description kde
KDE session support for %{name}.

%package gnome
Summary:	GNOME support for %{name}
Group:		Graphical desktop/GNOME
Requires:	%{name} = %{EVRD}

%description gnome
GNOME session support for %{name}.

%package -n %{libobrender}
Summary:	Libraries from openbox
Group:		System/Libraries
Obsoletes:	%{_lib}openbox27 < 3.5.0-8
Obsoletes:	%{_lib}openbox29 < 3.6.1-1

%description -n %{libobrender}
This package contains a shared library for %{name}.

%package -n %{libobt}
Summary:	Libraries from openbox
Group:		System/Libraries
Conflicts:	%{_lib}openbox27 < 3.5.0-8

%description -n %{libobt}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development files from openbox
Group:		Development/Other
Requires:	%{libobrender} = %{version}-%{release}
Requires:	%{libobt} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%prep
%setup -q -a1 -a2
%apply_patches
autoreconf -fi
2to3 -w data/autostart/openbox-xdg-autostart tools/themeupdate/themeupdate.py

%build
%configure --disable-static
%make DEFAULT_MENU=%{_sysconfdir}/xdg/openbox/menu.xml

%install
%makeinstall_std

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

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS CHANGELOG README
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

%files kde
%{_bindir}/openbox-kde-session
%{_datadir}/xsessions/openbox-kde.desktop
%{_mandir}/man1/openbox-kde-session.1.*

%files gnome
%{_bindir}/gdm-control
%{_bindir}/gnome-panel-control
%{_bindir}/openbox-gnome-session
%{_datadir}/xsessions/openbox-gnome.desktop
%{_datadir}/gnome-session/sessions/openbox-*.session
%{_datadir}/gnome/wm-properties/openbox.desktop
%{_mandir}/man1/openbox-gnome-session.1.*

%files -n %{libobrender}
%{_libdir}/libobrender.so.%{major}*

%files -n %{libobt}
%{_libdir}/libobt.so.%{obtmajor}*

%files -n %{devname}
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/%{name}
