%define		zope_subname CMF
Summary:	Content Management Framework for Zope
Summary(pl):	¦rodowisko zarz±dzania tre¶ci± dla Zope
Name:		Zope-%{zope_subname}
Version:	1.5.5
Release:	1
Epoch:		1
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://zope.org/Products/CMF/%{zope_subname}-%{version}/%{zope_subname}-%{version}.tar.gz
# Source0-md5:	301bf1cccefc1769614acf0fb3ba982c
URL:		http://cmf.zope.org/
BuildRequires:	python
%pyrequires_eq	python-modules
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	/usr/sbin/installzopeproduct
Requires:	Zope >= 2.7.7
Obsoletes:	CMF
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Content Management Framework (CMF) for Zope from Zope Corporation
delivers a powerful, tailored CMS in a fraction of the time of big
vendors.

%description -l pl
CMF to Content Management Framework, czyli ¶rodowisko zarz±dzania
tre¶ci± dla Zope. Dostarcza w krótkim czasie potê¿ny, dopasowany
system zarz±dzania tre¶ci± dla du¿ych producentów.

%prep
%setup -q -n %{zope_subname}-%{version}

%build
#mkdir docs
mkdir docs/CMFActionIcons docs/CMFCalendar docs/CMFCore docs/CMFDefault docs/CMFSetup docs/CMFTopic docs/DCWorkflow
mv -f CMFActionIcons/README.txt docs/CMFActionIcons
mv -f {CHANGES.txt,HISTORY.txt,INSTALL*,README.txt} docs/
mv -f CMFCalendar/{INSTALL.txt,README.txt,TODO.txt,CREDITS.txt} docs/CMFCalendar
mv -f CMFCore/README.txt docs/CMFCore
mv -f CMFDefault/README.txt docs/CMFDefault
mv -f CMFSetup/{CREDITS.txt,README.txt} docs/CMFSetup
mv -f CMFTopic/README.txt docs/CMFTopic
mv -f DCWorkflow/{README.txt,CHANGES.txt} docs/DCWorkflow

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af {CMFActionIcons,CMFCalendar,CMFCore,CMFDefault,CMFSetup,CMFTopic,CMFUid,DCWorkflow} $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in CMFActionIcons CMFCalendar CMFCore CMFDefault CMFSetup CMFTopic CMFUid DCWorkflow ; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
%service -q zope restart

%postun
if [ "$1" = "0" ]; then
	for p in CMFActionIcons CMFCalendar CMFCore CMFDefault CMFSetup CMFTopic CMFUid DCWorkflow ; do
		/usr/sbin/installzopeproduct -d $p
	done
	%service -q zope restart
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}
