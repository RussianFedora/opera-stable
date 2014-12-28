%define debug_package %{nil}
%define appname opera

Summary:        Web Browser for Linux
Summary(ru):    Веб-браузер для Linux
Name:           opera-stable
Version:    26.0.1656.60
Release:    4%{dist}
Epoch:      5

Group:      Applications/Internet
License:    Proprietary
URL:        http://www.opera.com/browser
Source0:    ftp://ftp.opera.com/pub/%{appname}/desktop/%{version}/linux/%{name}_%{version}_amd64.deb
Source1:    rfremix-%{name}.appdata.xml

BuildRequires:  desktop-file-utils
%if 0%{?fedora} >= 20
BuildRequires:  libappstream-glib
%endif
# BuildRequires:  chrpath

Provides:   libcrypto.so.1.0.0()(64bit)
Provides:   libcrypto.so.1.0.0(OPENSSL_1.0.0)(64bit)
Provides:   libssl.so.1.0.0()(64bit)
Provides:   libssl.so.1.0.0(OPENSSL_1.0.0)(64bit)
Provides:   libssl.so.1.0.0(OPENSSL_1.0.1)(64bit)
Provides:   libudev.so.0()(64bit)

ExclusiveArch:    x86_64

%description
Opera is a fast, secure and user-friendly web browser. It
includes web developer tools, news aggregation, and the ability
to compress data via Opera Turbo on congested networks.

%description -l ru
Opera — это быстрый, безопасный и дружественный к пользователю
веб-браузер. Он включает средства веб-разработки и сбора новостей,
а также возможность сжимать трафик в перегруженных сетях
посредством технологии Opera Turbo.

%prep
%setup -q -c -T

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# Extract DEB packages:
pushd %{buildroot}
    ar p %{SOURCE0} data.tar.xz | xz -d > %{name}-%{version}.x86_64.tar
    tar -xf %{name}-%{version}.x86_64.tar
popd

# Move /usr/lib/x86_64-linux-gnu/%{appname} to %{_libdir}/%{name}:
mv %{buildroot}/usr/lib/x86_64-linux-gnu/%{appname} %{buildroot}/usr/lib/%{name}
rm -rf %{buildroot}/usr/lib/x86_64-linux-gnu
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

# Modify DOC directory and *.desktop file:
mv %{buildroot}%{_datadir}/doc/%{name} %{buildroot}%{_datadir}/doc/%{name}-%{version}
mv %{buildroot}%{_datadir}/applications/%{appname}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's/Name=Opera/Name=Opera\ stable/g' -i %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's|Exec=%{appname}|Exec=%{name}|g' -i %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's|Icon=%{appname}|Icon=%{name}|g' -i %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's/TargetEnvironment=Unity/#TargetEnvironment=Unity/g' -i %{buildroot}%{_datadir}/applications/%{name}.desktop

# Rename icon files:
mv %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{appname}.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
mv %{buildroot}%{_datadir}/pixmaps/%{appname}.xpm %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# Install *.desktop file:
desktop-file-install --vendor rfremix \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category Network \
  --add-category WebBrowser \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Create necessary symbolic links
mkdir -p %{buildroot}%{_libdir}/%{name}/lib
pushd %{buildroot}%{_libdir}/%{name}/lib
    ln -s ../../libudev.so.1 libudev.so.0
    ln -s %{_libdir}/libcrypto.so.10 libcrypto.so.1.0.0
    ln -s %{_libdir}/libssl.so.10 libssl.so.1.0.0
popd

# Fix symlink:
pushd %{buildroot}%{_bindir}
    rm %{appname}
    %ifarch x86_64
        ln -s ../lib64/%{name}/%{appname} %{name}
    %else
        ln -s ../lib/%{name}/%{appname} %{name}
    %endif
popd

# Fix <opera_sandbox> attributes:
chmod 4755 %{buildroot}%{_libdir}/%{name}/opera_sandbox

# Remove unused directories and tarball:
pushd %{buildroot}
    rm %{name}-%{version}.x86_64.tar
    rm -rf %{buildroot}%{_datadir}/lintian
    rm -rf %{buildroot}%{_datadir}/menu
popd

## Remove rpath
# find %{buildroot} -name "opera_autoupdate" -exec chrpath --delete {} \; 2>/dev/null
# find %{buildroot} -name "opera_crashreporter" -exec chrpath --delete {} \; 2>/dev/null

# Install appstream data
%if 0%{?fedora} >= 20
    mkdir -p %{buildroot}%{_datadir}/appdata
    install -pm 644 %{SOURCE1} %{buildroot}%{_datadir}/appdata/rfremix-%{name}.appdata.xml
%endif

%if 0%{?fedora} >= 20
%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/rfremix-%{name}.appdata.xml
%endif

%post
update-desktop-database &> /dev/null || :
touch --no-create /usr/share/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache --quiet /usr/share/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create /usr/share/icons/hicolor &>/dev/null
    gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :

%clean
rm -rf %{buildroot}

%files
%{_defaultdocdir}/%{name}-%{version}
%{_bindir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/*
%{_datadir}/pixmaps/*
%if 0%{?fedora} >= 20
    %{_datadir}/appdata/rfremix-%{name}.appdata.xml
%endif

%changelog
* Sun Dec 28 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.60-4
- Fixed <files> section
- Remove RHEL >=8 condition
- Add <check> section

* Sat Dec 27 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.60-3
- Add appdata.xml for Fedora >=20 and RHEL >=8
- Remove category X-Fedora from *.desktop file

* Tue Dec 23 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.60-2
- Remove chrpath action:
  http://ruario.ghost.io/2014/12/15/opera-packages-for-fedora-with-updates/#comment-1755224247

* Wed Dec 17 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.60-1
- Update to 26.0.1656.60
- Clean up spec file

* Wed Dec 10 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.32-2
- Add BR: chrpath

* Wed Dec 03 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.32-1
- Rename to opera-stable according to new channel
- Update to 26.0.1656.32
- Remove wrapper scripts for opera_autoupdate and opera_crashreporter binaries
- Remove bundled libs from Ubuntu 12.04

* Mon Nov 17 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.20-1
- Update to 26.0.1656.20

* Mon Nov 10 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.17-1
- Update to 26.0.1656.17

* Wed Oct 29 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.8-1
- Update to 26.0.1656.8
- Update bundled libssl from Ubuntu 12.04 to 1.0.0_1.0.1-4ubuntu5.20

* Wed Oct 15 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1614.54-1
- Update to 25.0.1614.54

* Tue Oct 07 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1614.35-1
- Update to 25.0.1614.35
- Update bundled libssl from Ubuntu 12.04 to 1.0.0_1.0.1-4ubuntu5.18

* Tue Sep 30 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1614.31-1
- Update to 25.0.1614.31

* Wed Sep 24 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1614.18-1
- Update to 25.0.1614.18

* Fri Sep 19 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1614.11-1
- Rename to opera-beta according to new channel
- Update to 25.0.1614.11

* Sat Sep 13 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1614.5-1
- Update to 25.0.1614.5

* Fri Sep 05 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1613.1-1
- Update to 25.0.1613.1

* Thu Sep 04 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1606.0-1
- Update to 25.0.1606.0
- Fix paths at wrapper scripts for opera_autoupdate and opera_crashreporter
- Remove --force-native-window-frame=false from EXEC string at *.desktop file

* Wed Aug 20 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1597.0-1
- Update to 25.0.1597.0

* Sun Aug 17 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1592.0-1
- Update to 25.0.1592.0

* Tue Aug 12 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1583.1-2
- Update bundled libssl from Ubuntu 12.04 to 1.0.0_1.0.1-4ubuntu5.17
- Clean up spec file

* Fri Aug 08 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:25.0.1583.1-1
- Update to 25.0.1583.1
- Move /usr/lib/x86_64-linux-gnu/%{name} to %{_libdir}
- Clean up spec file

* Mon Aug 04 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 5:24.0.1558.21-3
- Remove BR: dpkg

* Tue Jul 29 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1558.21-2
- Hot fix: application icon does not appear in the KDE menu

* Tue Jul 29 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1558.21-1
- Update to 24.0.1558.21
- Add --force-native-window-frame=false to EXEC string at *.desktop file

* Fri Jul 25 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 5:24.0.1558.17-1
- Update to 24.0.1558.17

* Thu Jul 17 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 5:24.0.1558.3-1
- Update to 24.0.1558.3
- Correct build arch

* Fri Jun 27 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1555.0-1
- Update to 24.0.1555.0
- Remove bundled libudev.so.0 from Ubuntu 12.04
- Add wrapper scripts for opera_autoupdate and opera_crashreporter binaries
- Clean up spec file

* Fri Jun 27 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1543.0-1
- Update to 24.0.1543.0

* Fri Jun 27 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1537.0-3
- Fix bundled dependencies on libs from Ubuntu 12.04

* Tue Jun 24 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1537.0-2
- Apply libs from Ubuntu 12.04

* Mon Jun 23 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1537.0-1
- Update to 24.0.1537.0

* Mon Jul 29 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.16-1.R
- Update to 12.16

* Tue May 07 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.15-1.R
- Update to 12.15

* Fri Feb 15 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.14-2.R
- exclude badlinked opera_autoupdatechecker

* Thu Feb 14 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.14-1.R
- Update to 12.14

* Tue Nov 20 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.12-1.R
- Update to 12.12

* Tue Nov 20 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.11-1.R
- Update to 12.11

* Tue Nov 06 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.10-1.R
- Update to 12.10

* Fri Aug 31 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.02-1.R
- Update to 12.02

* Thu Jun 14 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.00-2.R
- Corrected spec for EL6

* Thu Jun 14 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.00-1.R
- Update to 12.00

* Thu May 10 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.64-1.R
- Update to 11.64

* Tue Mar 27 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.62-1.R
- Update to 11.62

* Tue Jan 24 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.61-1.R
- Added description in russian language
- Update to 11.61

* Wed Dec 07 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.60-1.R
- Added description in russian language
- Update to 11.60

* Wed Oct 19 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.52-1.R
- update to 11.52

* Thu Sep 01 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.51-1.R
- update to 11.51

* Mon Jun 27 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.50-1.R
- update to 11.50

* Tue Apr 12 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.10-2
- fix license window

* Tue Apr 12 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.10-1
- update to 11.10

* Thu Jan 27 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.01-1
- update to 11.01

* Thu Dec 16 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.00-1
- update to 11.00

* Tue Oct 12 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 5:10.63-2
- put 32bit binary to separate package

* Tue Oct 12 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.63-1
- update to 10.63

* Mon Sep 20 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.62-1
- update to 10.62

* Fri Aug 13 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.61-1
- update to 10.61

* Thu Jul  1 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.60-1
- update to 10.60

* Wed Jun 30 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.11-1
- update to 10.11

* Tue Jun  1 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.10-1
- update to 10.10

* Wed Oct 28 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.01-1
- update to 10.01

* Tue Sep 15 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-2
- qt4 version

* Mon Sep  7 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-1
- update to final 10.00

* Fri Jul 17 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-0.3.beta2
- update to beta2

* Wed Jun 24 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-0.2.beta1
- we had problem for F11 i586 arch in spec file. Fixed now.

* Wed Jun  3 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-0.1.beta1
- update to 10.00 beta 1

* Wed Mar  4 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 9.64-1
- update to 9.64

* Tue Dec 16 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.63-1
- update to 9.63

* Thu Oct 30 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.62-1
- update to 9.62

* Tue Oct 21 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.61-1
- update to 9.61

* Wed Oct  8 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.60-1
- update to 9.60

* Mon Aug 25 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.52-1
- update to 9.52

* Fri Jul  4 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.51-1
- update to 9.51

* Fri Jun 13 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.50-1
- final 9.50

* Thu Jun 12 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.50-0.2034
- update to RC

* Wed May 21 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.50b2-0.1
- add opera.desktop file

* Mon Apr 28 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.50b2-0
- update to 9.50b2

* Thu Apr  3 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.27-1
- 9.27

* Wed Feb 20 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.26-1
- 9.26

* Thu Dec 20 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.25-1
- 9.25

* Thu Aug 16 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.23-1
- 9.23

* Thu Jul 19 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.22-1
- 9.22

* Wed Jun 20 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.21-2
- add R for qt 3

* Thu May 17 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.21-1
- 9.21

* Thu Apr 12 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.20-0%{?dist}
- 9.20

* Fri Dec 22 2006 Arkady L. Shane <ashejn@yandex-team.ru> - 9.10-0%{?dist}
- 9.10

* Wed Jun 21 2006 Arkady L. Shane <shejn@msiu.ru> - 9.0-1%{?dist}
- rebuilt package with russian langpack
