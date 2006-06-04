Summary:	Sony Vaio SPIC Control Program
Name:		spicctrl
Version:	1.9
Release:	1
License:	GPL
Group:		Applications/System
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Source0:	http://popies.net/sonypi/%{name}-%{version}.tar.bz2
URL:		http://popies.net/sonypi/

%description
This utility allows one to query and set a variety of parameters on
your Sony Vaio laptop computer, including:

 - AC Power status
 - Battery status
 - Screen brightness
 - Bluetooth device power status

%prep
%setup -q
bzip2 -dc  %{_sourcedir}/%{name}-%{version}.tar.bz2 | tar xvf -
%build
%{__make}
%clean
rm -rf $RPM_BUILD_ROOT
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT/%{_mandir}/man1
install %{_builddir}/%{name}-%{version}/spicctrl $RPM_BUILD_ROOT%{_sbindir}
install %{_builddir}/%{name}-%{version}/spicctrl.1 $RPM_BUILD_ROOT/%{_mandir}/man1

%post
if [ ! -c /dev/sonypi ]; then
	rm -f /dev/sonypi
	mknod /dev/sonypi c 10 250
fi
if [ -e %{_sysconfdir}/modules.conf ]; then
grep 'alias char-major-10-250 sonypi' %{_sysconfdir}/modules.conf > /dev/null
	RETVAL=$?
	if [ $RETVAL -ne 0 ]; then
echo 'alias char-major-10-250 sonypi' >> %{_sysconfdir}/modules.conf
echo 'options sonypi minor=250' >> %{_sysconfdir}/modules.conf
	fi
fi
if [ -e %{_sysconfdir}/modprobe.conf ]; then
grep 'alias char-major-10-250 sonypi' %{_sysconfdir}/modprobe.conf > /dev/null
	RETVAL=$?
	if [ $RETVAL -ne 0 ]; then
echo 'alias char-major-10-250 sonypi' >> %{_sysconfdir}/modprobe.conf
echo 'options sonypi minor=250' >> %{_sysconfdir}/modprobe.conf
	fi
fi
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/spicctrl
%{_mandir}/man1/spicctrl.1*
%doc %attr(644,root,root) AUTHORS
%doc %attr(444,root,root) LICENSE
%doc %attr(444,root,root) CHANGES
