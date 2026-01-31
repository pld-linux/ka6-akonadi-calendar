#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		akonadi-calendar
Summary:	Akonadi Calendar
Name:		ka6-%{kaname}
Version:	25.12.1
Release:	3
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	ca8de1bc3d808d2b1c014c858efdfcf7
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Test-devel >= 5.9.0
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-akonadi-contacts-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka6-kcalutils-devel >= %{kdeappsver}
BuildRequires:	ka6-kidentitymanagement-devel >= %{kdeappsver}
BuildRequires:	ka6-kmailtransport-devel >= %{kdeappsver}
BuildRequires:	ka6-messagelib-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf6-kcodecs-devel >= %{kframever}
BuildRequires:	kf6-kcontacts-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
ExcludeArch:	x32 i686
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Akonadi Calendar is a library that effectively bridges the
type-agnostic API of the Akonadi client libraries and the
domain-specific KCalCore library. It provides jobs, models and other
helpers to make working with events and calendars through Akonadi
easier.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
/etc/xdg/autostart/org.kde.kalendarac.desktop
%attr(755,root,root) %{_bindir}/kalendarac
%{_libdir}/libKPim6AkonadiCalendar.so.*.*
%ghost %{_libdir}/libKPim6AkonadiCalendar.so.6
%ghost %{_libdir}/libKPim6AkonadiCalendarCore.so.6
%{_libdir}/libKPim6AkonadiCalendarCore.so.*.*
%{_libdir}/qt6/plugins/akonadi_serializer_kcalcore.so
%dir %{_libdir}/qt6/plugins/kf6/org.kde.kcalendarcore.calendars
%{_libdir}/qt6/plugins/kf6/org.kde.kcalendarcore.calendars/libakonadicalendarplugin.so
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_kcalcore.desktop
%{_datadir}/dbus-1/services/org.kde.kalendarac.service
%{_datadir}/knotifications6/kalendarac.notifyrc
%{_datadir}/qlogging-categories6/akonadi-calendar.categories
%{_datadir}/qlogging-categories6/akonadi-calendar.renamecategories
%{_datadir}/qlogging-categories6/org_kde_kalendarac.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/AkonadiCalendar
%{_includedir}/KPim6/AkonadiCalendarCore
%{_libdir}/cmake/KPim6AkonadiCalendar
%{_libdir}/cmake/KPim6AkonadiCalendarCore
%{_libdir}/libKPim6AkonadiCalendar.so
%{_libdir}/libKPim6AkonadiCalendarCore.so
