%include	/usr/lib/rpm/macros.python
%define		zope_subname	CMF
Summary:	Content Management Framework for Zope
Summary(pl):	¦rodowisko zarz±dzania tre¶ci± dla Zope
Name:		Zope-%{zope_subname}
Version:	1.3.3
Release:	5
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://cmf.zope.org/download/%{zope_subname}-%{version}/%{zope_subname}-%{version}.tar.gz
# Source0-md5:	ebe0a33f1cb8c4f61f23f8b84a0b7a5b
URL:		http://cmf.zope.org/
%pyrequires_eq	python-modules
Requires:	Zope
Requires(post,postun):  /usr/sbin/installzopeproduct
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
mkdir docs/CMFCalendar docs/CMFCore docs/CMFDefault docs/CMFTopic
mv -f *.txt docs/
mv -f CMFCalendar/*.txt docs/CMFCalendar
mv -f CMFCore/*.txt docs/CMFCore
mv -f CMFDefault/*.txt docs/CMFDefault
mv -f CMFTopic/*.txt docs/CMFTopic

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af * $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

#find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
for p in CMFCalendar CMFCore CMFDefault CMFTopic ; do
        /usr/sbin/installzopeproduct %{_datadir}/%{name}/$p
done
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%postun
if [ "$1" = "0" ]; then
        for p in CMFCalendar CMFCore CMFDefault CMFTopic ; do
                /usr/sbin/installzopeproduct -d $p
        done
fi
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%{_datadir}/%{name}
