%include	/usr/lib/rpm/macros.python
%define		zope_subname CMF
Summary:	Content Management Framework for Zope
Summary(pl):	¦rodowisko zarz±dzania tre¶ci± dla Zope
Name:		Zope-%{zope_subname}
Version:	1.4.3
%define		sub_ver rc1
%define		plone_ver CMFPlone2.0-rc6
%define		plone_dir CMFPlone-2.0-rc6
Release:	0.%{sub_ver}.1
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
#Source0:	http://cmf.zope.org/download/%{zope_subname}-%{version}/%{zope_subname}-%{version}-%{sub_ver}.tar.gz
Source0:        http://dl.sourceforge.net/sourceforge/plone/%{plone_ver}.tar.gz
# Source0-md5:  f6c03e49d910a6159f1810336941e92d
URL:		http://cmf.zope.org/
%pyrequires_eq	python-modules
Requires:	Zope
Requires(post,postun):	/usr/sbin/installzopeproduct
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
%setup -q -c %{plone_ver}

%build
mkdir docs
mkdir docs/CMFCalendar docs/CMFCore docs/CMFDefault docs/CMFTopic docs/DCWorkflow
#mv -f {CHANGES.txt,HISTORY.txt,INSTALL*,README.txt} docs/
mv -f %{plone_dir}/CMFCalendar/{INSTALL.txt,README.txt,TODO.txt,CREDITS.txt} docs/CMFCalendar
mv -f %{plone_dir}/CMFCore/README.txt docs/CMFCore
mv -f %{plone_dir}/CMFDefault/README.txt docs/CMFDefault
mv -f %{plone_dir}/CMFTopic/README.txt docs/CMFTopic
mv -f %{plone_dir}/DCWorkflow/{README.txt,CHANGES.txt} docs/DCWorkflow

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af %{plone_dir}/{CMFCalendar,CMFCore,CMFDefault,CMFTopic,DCWorkflow} $RPM_BUILD_ROOT%{_datadir}/%{name}

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
if [ "$1" = "0" ]; then
	for p in CMFCalendar CMFCore CMFDefault CMFTopic DCWorkflow ; do
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
