%define major 29
%define obtmajor 2
%define libobrender %mklibname obrender %{major}
%define libobt %mklibname obt %{obtmajor}
%define devname %mklibname -d %{name}

Summary:	Windowmanager based on the original blackbox-code
Name:		openbox
Version:	3.5.2
Release:	8
Group:		Graphical desktop/Other
License:	BSD
Url:		http://openbox.org/
Source0:	http://openbox.org/dist/openbox/%{name}-%{version}.tar.gz
Patch0:		openbox-3.5.0-mandriva_customisation.patch
Patch1:		openbox-3.5.2-unused-libs.patch
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pangoxft)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xcursor)
Requires:	xsetroot 
Suggests:	obconf 
Suggests:	rosa-elementary-theme

%description
Openbox is a window manager for the X11 windowing system.
It currently runs on a large list of platforms. It was originally
based on blackbox and currently remains very similar, even using
blackbox styles (with available extensions) for its themeing.

Openbox is the spawn of a number of previous blackbox users/hackers.
Being overall pleased with the window manager, but feeling left unable
to contribute, this project was born.The Openbox project is developed,
maintained, and contributed to by these individuals.

%package -n %{libobrender}
Summary:	Libraries from openbox
Group:		System/Libraries
Obsoletes:	%{_lib}openbox27 < 3.5.0-8

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
%setup -q
%apply_patches
autoreconf -fi

%build
%configure2_5x --disable-static
%make DEFAULT_MENU=%{_sysconfdir}/xdg/openbox/menu.xml

%install
%makeinstall_std

# session file
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat > %{buildroot}%{_sysconfdir}/X11/wmsession.d/26openbox << EOF
NAME=Openbox
ICON=%{_datadir}/pixmaps/openbox.png
EXEC=%{_bindir}/startopenbox
DESC=%Summary
SCRIPT:
exec %{_bindir}/startopenbox
EOF

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/start%{name} <<EOF
#!/bin/sh
%{_bindir}/xsetroot -solid Black
exec %{_bindir}/openbox-session
EOF

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS CHANGELOG README
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/26%{name}
%dir %{_sysconfdir}/xdg/%{name}
%config(noreplace) %{_sysconfdir}/xdg/%{name}/*
%{_libexecdir}/openbox-autostart
%{_libexecdir}/openbox-xdg-autostart
%{_mandir}/man1/*
%{_datadir}/xsessions/*
%{_datadir}/gnome-session/sessions/openbox-*.session
%{_datadir}/gnome/wm-properties/openbox.desktop
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_datadir}/themes/*

%files -n %{libobrender}
%{_libdir}/libobrender.so.%{major}*

%files -n %{libobt}
%{_libdir}/libobt.so.%{obtmajor}*

%files -n %{devname}
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/%{name}

