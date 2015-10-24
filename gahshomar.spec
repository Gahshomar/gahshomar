Name:           gahshomar
Version:        4.4.0
Release:        1%{?dist}
Summary:        A Persian (Jalali/Farsi) calendar

License:        GPLv3+
URL:            https://gahshomar.github.io/gahshomar/
Source:         %{name}-%{version}.tar.gz

BuildRequires:  yelp-tools gcc intltool itstool gtk+-devel glib2-devel libpeas-devel libjalali-devel python3-devel
Requires:       libpeas libjalali python3-gobject
Recommends:	libappindicator-gtk3


%description
 Provides a calendar interface which can be used to easily convert the dates.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc README COPYING ChangeLog AUTHORS NEWS
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/org.gahshomar.Gahshomar.gschema.xml
%{_datadir}/gnome-shell/extensions/%{name}@org.gahshomar.gahshomar/
%{_datadir}/help/C/%{name}/
%{_datadir}/icons/*/*/apps/*
%{_datadir}/locale/*/LC_MESSAGES/*
%{_libdir}/%{name}/
%{python3_sitelib}/%{name}/

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/HighContrast &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /bin/touch --no-create %{_datadir}/icons/HighContrast &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/HighContrast &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/HighContrast &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%clean
rm -rf %{buildroot}


%changelog
* Thu Oct 22 2015 makerpm
- 
