%define name      openbox
%define version   3.4.7.2
%define release   %mkrel 2
%define title     Openbox
%define Summary   Windowmanager based on the original blackbox-code

%define major 21
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary:          %Summary
Name:             %name
Version:          %version
Release:          %release
Group:            Graphical desktop/Other
License:          BSD
URL:              http://www.icculus.org/openbox/
Source:           http://icculus.org/openbox/releases/%name-%version.tar.gz
Patch0:           01_rc.xml.dpatch
Patch1:           02_fix_freedesktop_compliance.dpatch
Buildrequires:   X11-devel
Buildrequires:   glib2-devel
BuildRequires:   libxml2-devel
BuildRequires:   pango-devel
Requires:        xsetroot

BuildRoot:        %_tmppath/%name-%{version}

%description
Openbox is a window manager for the X11 windowing system.
It currently runs on a large list of platforms. It was originally
based on blackbox and currently remains very similar, even using
blackbox styles (with available extensions) for its themeing.

Openbox is the spawn of a number of previous blackbox users/hackers.
Being overall pleased with the window manager, but feeling left unable
to contribute, this project was born.The Openbox project is developed,
maintained, and contributed to by these individuals.

%package -n %libname
Summary: Libraries from openbox
Group: System/Libraries
Provides: lib%name = %version-%release

%description -n %libname
Openbox is a window manager for the X11 windowing system.
It currently runs on a large list of platforms. It was originally
based on blackbox and currently remains very similar, even using
blackbox styles (with available extensions) for its themeing.

Openbox is the spawn of a number of previous blackbox users/hackers.
Being overall pleased with the window manager, but feeling left unable
to contribute, this project was born.The Openbox project is developed,
maintained, and contributed to by these individuals.

%package -n %develname
Summary: Development files from openbox
Group: Development/Other
Requires: %libname = %version-%release
Provides: lib%name-devel = %version-%release
Provides: %name-devel = %version-%release
Obsoletes: %mklibname -d openbox 1

%description -n %develname
Openbox is a window manager for the X11 windowing system.
It currently runs on a large list of platforms. It was originally
based on blackbox and currently remains very similar, even using
blackbox styles (with available extensions) for its themeing.

Openbox is the spawn of a number of previous blackbox users/hackers.
Being overall pleased with the window manager, but feeling left unable
to contribute, this project was born.The Openbox project is developed,
maintained, and contributed to by these individuals.

%prep
%setup -q

%patch0 -p1
%patch1 -p1

%build
%define __libtoolize /bin/true

%configure2_5x
%make DEFAULT_MENU=%_sysconfdir/xdg/openbox/menu.xml


%install
%__rm -rf %buildroot

%makeinstall_std

# session file
%__mkdir -p %buildroot%_sysconfdir/X11/wmsession.d
%__cat > %buildroot%_sysconfdir/X11/wmsession.d/25openbox << EOF
NAME=Openbox
ICON=%_datadir/pixmaps/openbox.png
EXEC=%_bindir/startopenbox
DESC=%Summary
SCRIPT:
exec %_bindir/startopenbox
EOF

%__mkdir -p %buildroot%_bindir
cat > %buildroot%_bindir/start%name <<EOF
%_bindir/xsetroot -solid Black
exec %_bindir/openbox
EOF

%find_lang %name

%post
%make_session

%postun
%make_session

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
%__rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS CHANGELOG README
%attr(755,root,root) %_bindir/*

#%config(noreplace) %_sysconfdir/menu-methods/%name
%config(noreplace) %_sysconfdir/X11/wmsession.d/25%name

%dir %_sysconfdir/xdg/%name
%config(noreplace) %_sysconfdir/xdg/%name/*
%{_libdir}/openbox/xdg-autostart
%{_datadir}/man/man1/*
%{_datadir}/xsessions/*

%_datadir/gnome/wm-properties/*
%_datadir/pixmaps/*
%_datadir/themes/*

%files -n %libname
%defattr(-,root,root)
%_libdir/*.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%_libdir/pkgconfig/*.pc
%_libdir/*.so
%_libdir/*.la
%_libdir/*.a
%_includedir/%name
