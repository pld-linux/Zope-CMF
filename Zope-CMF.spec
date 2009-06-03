%define		zope_subname CMF
Summary:	Content Management Framework for Zope
Summary(pl.UTF-8):	Środowisko zarządzania treścią dla Zope
Name:		Zope-%{zope_subname}
Version:	2.1.1
Release:	1
Epoch:		1
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://zope.org/Products/CMF/%{zope_subname}-%{version}/%{zope_subname}-%{version}.tar.gz
# Source0-md5:	769a487678e2f6cccfb1a3e970921c79
URL:		http://cmf.zope.org/
BuildRequires:	python
%pyrequires_eq	python-modules
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	/usr/sbin/installzopeproduct
Requires:	Zope >= 2.10.4
Obsoletes:	CMF
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Content Management Framework (CMF) for Zope from Zope Corporation
delivers a powerful, tailored CMS in a fraction of the time of big
vendors.

%description -l pl.UTF-8
CMF to Content Management Framework, czyli środowisko zarządzania
treścią dla Zope. Dostarcza w krótkim czasie potężny, dopasowany
system zarządzania treścią dla dużych producentów.

%prep
%setup -q -n %{zope_subname}-%{version}

%build
#mkdir docs
mkdir docs/CMFActionIcons docs/CMFCalendar docs/CMFCore docs/CMFDefault docs/CMFTopic docs/DCWorkflow docs/GenericSetup
mv -f CMFActionIcons/README.txt docs/CMFActionIcons
mv -f {CHANGES.txt,HISTORY.txt,INSTALL*,README.txt} docs/
mv -f CMFCalendar/{README.txt,CREDITS.txt} docs/CMFCalendar
mv -f CMFCore/README.txt docs/CMFCore
mv -f CMFDefault/README.txt docs/CMFDefault
mv -f GenericSetup/{CREDITS.txt,README.txt} docs/GenericSetup
mv -f DCWorkflow/README.txt docs/DCWorkflow

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af {CMFActionIcons,CMFCalendar,CMFCore,CMFDefault,CMFTopic,CMFUid,DCWorkflow,GenericSetup} $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in CMFActionIcons CMFCalendar CMFCore CMFDefault CMFTopic CMFUid DCWorkflow GenericSetup; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
%service -q zope restart

%postun
if [ "$1" = "0" ]; then
	for p in CMFActionIcons CMFCalendar CMFCore CMFDefault CMFTopic CMFUid DCWorkflow GenericSetup ; do
		/usr/sbin/installzopeproduct -d $p
	done
	%service -q zope restart
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}
