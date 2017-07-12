%global build_for_x86_64 1
%global build_for_i386 0
%global build_from_rpm 1
%define debug_package %{nil}
%define appname opera

Summary:        Fast and secure web browser
Summary(ru):    Быстрый и безопасный Веб-браузер
Name:           opera-stable
Version:    46.0.2597.46
%if 0%{?fedora} >= 25
Release:	1%{?dist}.R
%else
Release:	1%{?dist}
%endif
Epoch:      5

Group:      Applications/Internet
License:    Proprietary
URL:        http://www.opera.com/browser

%if 0%{?build_for_x86_64}
%if 0%{?build_from_rpm}
Source0:    http://ftp.opera.com/pub/%{appname}/desktop/%{version}/linux/%{name}_%{version}_amd64.rpm
%else
Source0:    http://ftp.opera.com/pub/%{appname}/desktop/%{version}/linux/%{name}_%{version}_amd64.deb
%endif
%endif

%if 0%{?build_for_i386}
%if 0%{?build_from_rpm}
Source1:    http://ftp.opera.com/pub/%{appname}/desktop/%{version}/linux/%{name}_%{version}_i386.rpm
%else
Source1:    http://ftp.opera.com/pub/%{appname}/desktop/%{version}/linux/%{name}_%{version}_i386.deb
%endif
%endif

Source2:    rfremix-%{name}.appdata.xml

Requires:   hicolor-icon-theme

BuildRequires:  desktop-file-utils

%if 0%{?fedora} >= 20
BuildRequires:  libappstream-glib
%endif

# BuildRequires:  chrpath

# Provides:   libcrypto.so.1.0.0()(64bit)
# Provides:   libcrypto.so.1.0.0(OPENSSL_1.0.0)(64bit)
# Provides:   libudev.so.0()(64bit)
%ifarch x86_64
Provides:   libssl.so.1.0.0()(64bit)
Provides:   libssl.so.1.0.0(OPENSSL_1.0.0)(64bit)
Provides:   libssl.so.1.0.0(OPENSSL_1.0.1)(64bit)
Provides:   libffmpeg.so()(64bit)
%else
Provides:   libssl.so.1.0.0
Provides:   libssl.so.1.0.0(OPENSSL_1.0.0)
Provides:   libssl.so.1.0.0(OPENSSL_1.0.1)
Provides:   libffmpeg.so
%endif

%if 0%{?build_for_x86_64}
%if !0%{?build_for_i386}
ExclusiveArch:    x86_64
%else
ExclusiveArch:    x86_64 i686
%endif
%else
%if 0%{?build_for_i386}
ExclusiveArch:    i686
%endif
%endif

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

# Extract DEB/RPM packages:
pushd %{buildroot}
    %ifarch x86_64
        %if 0%{?build_from_rpm}
            rpm2cpio %{SOURCE0} | cpio -idV --quiet
        %else
            ar p %{SOURCE0} data.tar.xz | xz -d > %{name}-%{version}.x86_64.tar
            tar -xf %{name}-%{version}.x86_64.tar
        %endif
    %else
        %if 0%{?build_from_rpm}
            rpm2cpio %{SOURCE1} | cpio -idV --quiet
        %else
            ar p %{SOURCE1} data.tar.xz | xz -d > %{name}-%{version}.i386.tar
            tar -xf %{name}-%{version}.i386.tar
        %endif
    %endif
popd

# Move /usr/lib/%{arch}-linux-gnu/%{appname} to %{_libdir}/%{name} (for DEB source):
%if !0%{?build_from_rpm}
    %ifarch x86_64
        mv %{buildroot}/usr/lib/x86_64-linux-gnu/%{appname} %{buildroot}/usr/lib/%{name}
        rm -rf %{buildroot}/usr/lib/x86_64-linux-gnu
        mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
    %else
        mv %{buildroot}%{_libdir}/i386-linux-gnu/%{appname} %{buildroot}%{_libdir}/%{name}
        rm -rf %{buildroot}%{_libdir}/i386-linux-gnu
    %endif
%else
    mv %{buildroot}%{_libdir}/%{appname} %{buildroot}%{_libdir}/%{name}
%endif

# Modify DOC directory, *.desktop file and ffmpeg_preload_config.json:
if [ -d %{buildroot}%{_datadir}/doc/%{name}/ ]; then
    mv %{buildroot}%{_datadir}/doc/%{name} %{buildroot}%{_datadir}/doc/%{name}-%{version}
else
    mkdir -p %{buildroot}%{_datadir}/doc/%{name}-%{version}
fi
mv %{buildroot}%{_datadir}/applications/%{appname}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's/Name=Opera/Name=Opera\ stable/g' -i %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's|Exec=%{appname}|Exec=%{name}|g' -i %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's|Icon=%{appname}|Icon=%{name}|g' -i %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's/TargetEnvironment=Unity/#TargetEnvironment=Unity/g' -i %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's|/usr/lib/chromium-browser/libs|%{_libdir}/%{name}/lib_extra|g' -i %{buildroot}%{_libdir}/%{name}/resources/ffmpeg_preload_config.json

# Rename icon files:
mv %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{appname}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
mv %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{appname}.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
mv %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{appname}.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
mv %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{appname}.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
mv %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{appname}.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
mv %{buildroot}%{_datadir}/pixmaps/%{appname}.xpm %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# Install *.desktop file:
desktop-file-install --vendor rfremix \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category Network \
  --add-category WebBrowser \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Create necessary symbolic link
mkdir -p %{buildroot}%{_libdir}/%{name}/lib
pushd %{buildroot}%{_libdir}/%{name}/lib
#   ln -s ../../libudev.so.1 libudev.so.0
#   ln -s %{_libdir}/libcrypto.so.10 libcrypto.so.1.0.0
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

# Remove unused directories and tarball (for DEB source):
%if !0%{?build_from_rpm}
    pushd %{buildroot}
        %ifarch x86_64
            rm %{name}-%{version}.x86_64.tar
        %else
            rm %{name}-%{version}.i386.tar
        %endif
        rm -rf %{buildroot}%{_datadir}/lintian
        rm -rf %{buildroot}%{_datadir}/menu
    popd
%endif

## Remove rpath
# find %{buildroot} -name "opera_autoupdate" -exec chrpath --delete {} \; 2>/dev/null
# find %{buildroot} -name "opera_crashreporter" -exec chrpath --delete {} \; 2>/dev/null

# Install appstream data
%if 0%{?fedora} >= 20
    mkdir -p %{buildroot}%{_datadir}/appdata
    install -pm 644 %{SOURCE2} %{buildroot}%{_datadir}/appdata/rfremix-%{name}.appdata.xml

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
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/mime/packages/*
%{_datadir}/pixmaps/*.xpm
%if 0%{?fedora} >= 20
%{_datadir}/appdata/rfremix-%{name}.appdata.xml
%endif

%changelog
* Wed Jul 12 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:46.0.2597.46-1
- Update to 46.0.2597.46

* Thu Jul 06 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:46.0.2597.39-1
- Update to 46.0.2597.39

* Tue Jun 27 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:46.0.2597.32-1
- Update to 46.0.2597.32

* Wed Jun 21 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:46.0.2597.26-1
- Update to 46.0.2597.26

* Tue Jun 13 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:45.0.2552.898-1
- Update to 45.0.2552.898

* Thu Jun 01 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:45.0.2552.888-1
- Update to 45.0.2552.888

* Fri May 26 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:45.0.2552.881-1
- Update to 45.0.2552.881

* Mon May 15 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:45.0.2552.812-1
- Update to 45.0.2552.812

* Tue May 09 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:45.0.2552.635-1
- Update to 45.0.2552.635

* Tue Apr 25 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:44.0.2510.1449-1
- Update to 44.0.2510.1449

* Fri Apr 21 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:44.0.2510.1218-2
- Fixed <files> section

* Wed Apr 12 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:44.0.2510.1218-1
- Update to 44.0.2510.1218

* Wed Apr 05 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:44.0.2510.1159-1
- Update to 44.0.2510.1159

* Sat Mar 25 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:44.0.2510.857-1
- Update to 44.0.2510.857

* Wed Mar 01 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:43.0.2442.1144-1
- Update to 43.0.2442.1144

* Wed Feb 22 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:43.0.2442.991-1
- Update to 43.0.2442.991

* Thu Feb 07 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:43.0.2442.806-1
- Update to 43.0.2442.806

* Thu Jan 26 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:42.0.2393.517-1
- Update to 42.0.2393.517

* Tue Jan 24 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:42.0.2393.351-1
- Update to 42.0.2393.351

* Thu Jan 19 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:42.0.2393.137-2
- Fix bogus date

* Thu Jan 19 2017 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:42.0.2393.137-1
- Update to 42.0.2393.137

* Fri Dec 23 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:42.0.2393.94-1
- Update to 42.0.2393.94

* Wed Dec 14 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:42.0.2393.85-1
- Update to 42.0.2393.85

* Tue Nov 22 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:41.0.2353.69-1
- Update to 41.0.2353.69

* Tue Nov 08 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:41.0.2353.56-1
- Update to 41.0.2353.56

* Tue Oct 25 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:41.0.2353.46-1
- Update to 41.0.2353.46

* Tue Oct 18 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:40.0.2308.90-1
- Update to 40.0.2308.90

* Fri Sep 23 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:40.0.2308.81-1
- Update to 40.0.2308.81

* Fri Sep 23 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:40.0.2308.62-1
- Update to 40.0.2308.62

* Tue Sep 20 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:40.0.2308.54-1
- Update to 40.0.2308.54

* Tue Sep 06 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:39.0.2256.71-1
- Update to 39.0.2256.71

* Mon Aug 08 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:39.0.2256.48-1
- Update to 39.0.2256.48

* Wed Aug 03 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:39.0.2256.43-1
- Update to 39.0.2256.43

* Mon Jul 04 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:38.0.2220.41-1
- Update to 38.0.2220.41

* Tue Jun 14 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:38.0.2220.31-1
- Update to 38.0.2220.31

* Tue Jun 07 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:38.0.2220.29-1
- Update to 38.0.2220.29

* Fri Jun 03 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:37.0.2178.54-1
- Update to 37.0.2178.54

* Mon May 09 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:37.0.2178.43-1
- Update to 37.0.2178.43

* Wed May 04 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:37.0.2178.32-1
- Update to 37.0.2178.32

* Tue Apr 12 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:36.0.2130.65-1
- Update to 36.0.2130.65

* Thu Mar 31 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:36.0.2130.46-1
- Update to 36.0.2130.46

* Mon Mar 14 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:36.0.2130.32-1
- Update to 36.0.2130.32
- Fix ffmpeg_preload_config.json

* Tue Mar 01 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.92-1
- Update to 35.0.2066.92

* Mon Feb 22 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.82-1
- Update to 35.0.2066.82

* Tue Feb 16 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.68-1
- Update to 35.0.2066.68

* Wed Feb 03 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.37-3
- Fix executable symlink path

* Mon Feb 01 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.37-2
- Fix executable symlink creation

* Mon Feb 01 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:35.0.2066.37-1
- Update to 35.0.2066.37

* Tue Jan 19 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:34.0.2036.50-1
- Update to 34.0.2036.50

* Tue Jan 12 2016 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:34.0.2036.47-1
- Update to 34.0.2036.47

* Tue Dec 08 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:34.0.2036.25-1
- Update to 34.0.2036.25
- Add switchers for RPM / DEB source packages

* Mon Nov 30 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:33.0.1990.137-1
- Update to 33.0.1990.137

* Tue Nov 17 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:33.0.1990.115-1
- Update to 33.0.1990.115

* Mon Nov 02 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:33.0.1990.58-1
- Update to 33.0.1990.58

* Wed Oct 28 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:33.0.1990.43-1
- Update to 33.0.1990.43

* Mon Sep 28 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:32.0.1948.69-1
- Update to 32.0.1948.69

* Tue Sep 15 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:32.0.1948.25-1
- Update to 32.0.1948.25

* Tue Aug 18 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:31.0.1889.174-1
- Update to 31.0.1889.174

* Tue Aug 04 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:31.0.1889.99-2
- Add Provides: libssl.so.1.0.0
- Fix <provides> section for 32 bit builds

* Tue Aug 04 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:31.0.1889.99-1
- Update to 31.0.1889.99

* Wed Jul 15 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:30.0.1835.125-1
- Update to 30.0.1835.125

* Wed Jun 24 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:30.0.1835.88-1
- Update to 30.0.1835.88

* Sun Jun 14 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:30.0.1835.59-1
- Update to 30.0.1835.59

* Wed Jun 10 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:30.0.1835.52-1
- Update to 30.0.1835.52

* Wed May 20 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:29.0.1795.60-1
- Update to 29.0.1795.60

* Sat May 09 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:29.0.1795.47-2
- Bump version for Fedora >= 22

* Wed Apr 29 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:29.0.1795.47-1
- Update to 29.0.1795.47

* Wed Apr 08 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:28.0.1750.51-1
- Update to 28.0.1750.51

* Wed Mar 18 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:28.0.1750.48-1
- Update to 28.0.1750.48

* Tue Mar 10 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:28.0.1750.40-1
- Update to 28.0.1750.40

* Tue Feb 24 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:27.0.1689.76-1
- Update to 27.0.1689.76

* Wed Feb 11 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:27.0.1689.69-1
- Update to 27.0.1689.69

* Tue Feb 03 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:27.0.1689.66-1
- Update to 27.0.1689.66

* Tue Jan 27 2015 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:27.0.1689.54-1
- Update to 27.0.1689.54

* Mon Dec 29 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.60-4.1
- Remove <icon>, <categories> and <architectures> sections from *.appdata.xml

* Sun Dec 28 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.60-4
- Fixed <files> section
- Remove RHEL >=8 condition
- Add <check> section

* Sat Dec 27 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:26.0.1656.60-3
- Add *.appdata.xml for Fedora >=20 and RHEL >=8
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
