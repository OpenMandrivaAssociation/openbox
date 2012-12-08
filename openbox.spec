%define name      openbox
%define version   3.5.0
%define subrel 1
%define release   7
%define title     Openbox
%define Summary   Windowmanager based on the original blackbox-code

%define major 27
%define obtmajor 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary:          %Summary
Name:             %name
Version:          %version
Release:          %release
Group:            Graphical desktop/Other
License:          BSD
URL:              http://openbox.org/
Source:           http://openbox.org/dist/openbox/%name-%version.tar.gz
Patch0:		 openbox-3.5.0-mandriva_customisation.patch
Patch1:		 openbox-3.5.0-link.patch
BuildRequires:   libxext-devel
BuildRequires:   libxrandr-devel
BuildRequires:   libxinerama-devel
BuildRequires:   libxcursor-devel
BuildRequires:   pkgconfig(glib-2.0)
BuildRequires:   pkgconfig(libxml-2.0)
BuildRequires:   pango-devel
BuildRequires:   pkgconfig(pangoxft)
BuildRequires:   gettext-devel
BuildRequires:   startup-notification-devel >= 0.8
Requires:        xsetroot 
Suggests:	 rosa-elementary-theme
Suggests:        obconf 

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
%apply_patches

%build
autoreconf -fi
%configure2_5x
%make DEFAULT_MENU=%_sysconfdir/xdg/openbox/menu.xml

%install
%__rm -rf %buildroot

%makeinstall_std

# session file
%__mkdir -p %buildroot%_sysconfdir/X11/wmsession.d
%__cat > %buildroot%_sysconfdir/X11/wmsession.d/26openbox << EOF
NAME=Openbox
ICON=%_datadir/pixmaps/openbox.png
EXEC=%_bindir/startopenbox
DESC=%Summary
SCRIPT:
exec %_bindir/startopenbox
EOF

%__mkdir -p %buildroot%_bindir
cat > %buildroot%_bindir/start%name <<EOF
#!/bin/sh
%_bindir/xsetroot -solid Black
exec %_bindir/openbox-session
EOF

%find_lang %name

find %buildroot -name *.la | xargs rm

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS CHANGELOG README
%attr(755,root,root) %_bindir/*

#%config(noreplace) %_sysconfdir/menu-methods/%name
%config(noreplace) %_sysconfdir/X11/wmsession.d/26%name

%dir %_sysconfdir/xdg/%name
%config(noreplace) %_sysconfdir/xdg/%name/*
%_libexecdir/openbox-autostart
%_libexecdir/openbox-xdg-autostart
%{_datadir}/man/man1/*
%{_datadir}/xsessions/*

%_datadir/gnome/wm-properties/openbox.desktop
%_datadir/applications/*.desktop
%_datadir/pixmaps/*
%_datadir/themes/*

%files -n %libname
%defattr(-,root,root)
%_libdir/*.so.%{major}*
%defattr(-,root,root)
%_libdir/libobt.so.%{obtmajor}
%_libdir/libobt.so.%{obtmajor}.*

%files -n %develname
%defattr(-,root,root)
%_libdir/pkgconfig/*.pc
%_libdir/*.so
%_libdir/*.a
%_includedir/%name


%changelog
* Wed Oct 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.5.0-1.1
- built for updates

* Sun Oct 02 2011 ÐÐ»ÐµÐºÑÐ°Ð½Ð´Ñ€ ÐšÐ°Ð·Ð°Ð½Ñ†ÐµÐ² <kazancas@mandriva.org> 3.5.0-1
+ Revision: 702414
- new version 3.5.0
- set elementary as default theme
- add requires of elementary theme, which consists openbox theme
- drop old part of specs (< 2010)

* Mon Jun 13 2011 ÐÐ»ÐµÐºÑÐ°Ð½Ð´Ñ€ ÐšÐ°Ð·Ð°Ð½Ñ†ÐµÐ² <kazancas@mandriva.org> 3.4.11.2-7
+ Revision: 684683
- remove oxygen theme and elementary due move to theme package

* Wed May 04 2011 ÐÐ»ÐµÐºÑÐ°Ð½Ð´Ñ€ ÐšÐ°Ð·Ð°Ð½Ñ†ÐµÐ² <kazancas@mandriva.org> 3.4.11.2-5
+ Revision: 665863
- add oxygen theme

* Sun May 01 2011 Funda Wang <fwang@mandriva.org> 3.4.11.2-4
+ Revision: 661319
- add elementary theme

* Wed Dec 01 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 3.4.11.2-3mdv2011.0
+ Revision: 604522
- Replace X11-devel BR with only the needed libraries
  This saves around 60 package dependencies

* Sun Jul 25 2010 Ahmad Samir <ahmadsamir@mandriva.org> 3.4.11.2-2mdv2011.0
+ Revision: 559465
- suggest obconf (mdv#59732)

* Sun Jul 11 2010 Funda Wang <fwang@mandriva.org> 3.4.11.2-1mdv2011.0
+ Revision: 550586
- update to new version 3.4.11.2

* Fri Mar 26 2010 Funda Wang <fwang@mandriva.org> 3.4.11.1-1mdv2010.1
+ Revision: 527730
- New version 3.4.11
- 3 patches merged

* Wed Feb 24 2010 Michael Scherer <misc@mandriva.org> 3.4.11-2mdv2010.1
+ Revision: 510728
- fix rpmlint warning about shebang
- fix rpmlint warning about %%post
- do not disable format string gcc check, and use patch from upstream
- add comments about patchs sent to openbox developers
- fix the openbox starting script, fix #57749 thanks to dadada

  + Funda Wang <fwang@mandriva.org>
    - update source url
    - update URL

* Tue Feb 09 2010 Funda Wang <fwang@mandriva.org> 3.4.11-1mdv2010.1
+ Revision: 502586
- New version 3.4.11

* Fri Jan 08 2010 Frederik Himpe <fhimpe@mandriva.org> 3.4.10-1mdv2010.1
+ Revision: 487718
- update to new version 3.4.10

* Sun Dec 20 2009 Funda Wang <fwang@mandriva.org> 3.4.9-1mdv2010.1
+ Revision: 480317
- fix file list
- new version 3.4.9

* Thu Dec 10 2009 Funda Wang <fwang@mandriva.org> 3.4.8-1mdv2010.1
+ Revision: 476107
- new version 3.4.8

* Sun Aug 16 2009 Jani VÃ¤limaa <wally@mandriva.org> 3.4.7.2-5mdv2010.0
+ Revision: 416944
- fix gnome-settings-daemon path in one script (#49240)
- fix build

* Tue Jan 20 2009 JÃ©rÃ´me Soyer <saispo@mandriva.org> 3.4.7.2-4mdv2009.1
+ Revision: 331937
- Fix desktop file
- Rediff patch0

  + Anne Nicolas <ennael@mandriva.org>
    - increase order to avoid openbox being launched instead of LXDE by default

* Wed Sep 03 2008 Frederic Crozat <fcrozat@mandriva.com> 3.4.7.2-3mdv2009.0
+ Revision: 279722
- Update patch1 to work with latest gnome-session

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 3.4.7.2-2mdv2009.0
+ Revision: 268350
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat May 03 2008 Funda Wang <fwang@mandriva.org> 3.4.7.2-1mdv2009.0
+ Revision: 200690
- New version 3.4.7.2

* Thu Feb 07 2008 Funda Wang <fwang@mandriva.org> 3.4.6.1-1mdv2008.1
+ Revision: 163360
- New version 3.4.6.1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Mon Oct 22 2007 JÃ©rÃ´me Soyer <saispo@mandriva.org> 3.4.4-1mdv2008.1
+ Revision: 101163
- Add BR
- New release 3.4.4
- temp
- temp

* Mon Aug 06 2007 Frederic Crozat <fcrozat@mandriva.com> 3.3.1-2mdv2008.0
+ Revision: 59352
- Fix incorrect path for wmsession file


* Sat Dec 30 2006 Olivier Thauvin <nanardon@mandriva.org> 3.3.1-1mdv2007.0
+ Revision: 102819
- 3.3.1

* Sun Jul 16 2006 Olivier Thauvin <nanardon@mandriva.org> 3.2-2mdv2007.0
+ Revision: 41300
- fix path in script
- build the from the spec
- adjust requirement
- do no longer use X11R6 dir
- rebuild
- spec cleanup
- Import openbox

* Thu Apr 22 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 3.2-1mdk
- 3.2

* Mon Jan 05 2004 Götz Waschk <waschk@linux-mandrake.com> 3.1-2mdk
- fix buildrequires
- remove broken menu script
- fix description
- fix startopenbox script
- move files around

