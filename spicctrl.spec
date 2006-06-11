Summary:	Sony Vaio SPIC Control Program
Summary(pl):	Program do sterowania Sony Vaio SPIC
Name:		spicctrl
Version:	1.9
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://popies.net/sonypi/%{name}-%{version}.tar.bz2
# Source0-md5:	775a1959c03e59830303b8320ca379d2
URL:		http://popies.net/sonypi/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This utility allows one to query and set a variety of parameters on
your Sony Vaio laptop computer, including:

 - AC Power status
 - Battery status
 - Screen brightness
 - Bluetooth device power status

%description -l pl
To narzêdzie pozwala sprawdzaæ i ustawiaæ ró¿ne parametry laptopa Sony
Vaio, w tym:

 - stan zasilania AC
 - stan baterii
 - jasno¶æ ekranu
 - stan zasilania urzêdzenia Bluetooth

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -W"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1}

install spicctrl $RPM_BUILD_ROOT%{_sbindir}
install spicctrl.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post
# TODO: move to dev
if [ ! -c /dev/sonypi ]; then
	rm -f /dev/sonypi
	mknod /dev/sonypi c 10 250
fi
# TODO: use modprobe.d
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
%doc AUTHORS CHANGES
%attr(755,root,root) %{_sbindir}/spicctrl
%{_mandir}/man1/spicctrl.1*
