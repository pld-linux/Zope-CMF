%include	/usr/lib/rpm/macros.python
%define		zope_subname CMF
Summary:	Content Management Framework for Zope
Summary(pl):	¦rodowisko zarz±dzania tre¶ci± dla Zope
Name:		Zope-%{zope_subname}
Version:	1.4.2
Release:	3
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://cmf.zope.org/download/%{zope_subname}-%{version}/%{zope_subname}-%{version}.tar.gz
# Source0-md5:	345f8f79ce68d5535933ee897782005b
URL:		http://cmf.zope.org/
%pyrequires_eq	python-modules
Requires:	Zope
Requires(pre):	/usr/sbin/installzopeproduct
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{zope_subname}-%{version}-root-%(id -u -n)

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
mkdir docs/CMFCalendar docs/CMFCore docs/CMFDefault docs/CMFTopic docs/DCWorkflow
mv -f {CHANGES.txt,HISTORY.txt,INSTALL*,README.txt} docs/
mv -f CMFCalendar/{INSTALL.txt,README.txt,TODO.txt,CREDITS.txt} docs/CMFCalendar
mv -f CMFCore/README.txt docs/CMFCore
mv -f CMFDefault/README.txt docs/CMFDefault
mv -f CMFTopic/README.txt docs/CMFTopic
mv -f DCWorkflow/{README.txt,CHANGES.txt} docs/DCWorkflow

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af * $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in CMFCalendar CMFCore CMFDefault CMFTopic DCWorkflow ; do
	/usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
for p in CMFCalendar CMFCore CMFDefault CMFTopic DCWorkflow ; do
	/usr/sbin/installzopeproduct -d $p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}/all_cmf_tests.*
%{_datadir}/%{name}/slurp*
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/CMFCalendar
%{_datadir}/%{name}/CMFCore
%{_datadir}/%{name}/CMFDefault
%{_datadir}/%{name}/CMFTopic
%{_datadir}/%{name}/DCWorkflow
