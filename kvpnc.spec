%define name    kvpnc
%define version 0.8.9
%define rel     1
%define release %mkrel %rel
%define Summary KDE frontend to various vpn clients

%define unstable 1
%define use_enable_final 1

Summary:        %{Summary}
Name:           %{name}
Version:        %{version}
Release:        %{release}

License: 		GPL
Group: 			Graphical desktop/KDE
Source: 		http://download.gna.org/kvpnc/kvpnc-%{version}.tar.bz2
URL: 			http://home.gna.org/kvpnc/

BuildRoot: 		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	kdelibs-devel
BuildRequires:  libgcrypt-devel
Requires: 		usermode-consoleonly
Requires: 		kvpnc-backend


%description
KVpnc is a KDE frontend for for various vpn clients.
It supports Cisco VPN (vpnc) and IPSec (FreeS/WAN, racoon).
Vpnc is a replacement for the cisco VPN client and its used 
as client for the cisco3000 VPN Concentrator, FreeS/WAN (OpenS/WAN) 
is a IPSec client for Linux 2.4.x and racoon is a IPSec client 
for Linux 2.6.x and *BSD.

%prep
%setup -q -n kvpnc-%{version}

%build

%configure --disable-rpath \
%if %use_enable_final
			--enable-final \
%else		
			--disable-final \
%endif
%if "%{_lib}" != "lib"
    --enable-libsuffix="%(A=%{_lib}; echo ${A/lib/})" \
%endif
%if %unstable
					--enable-debug=full 
%else
					--disable-debug 
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall

# Menu

install -d $RPM_BUILD_ROOT%{_menudir}
kdedesktop2mdkmenu.pl %{name} "Internet/Remote Access" $RPM_BUILD_ROOT%{_datadir}/applnk/kvpnc.desktop $RPM_BUILD_ROOT%{_menudir}/%{name}

%find_lang %{name}

#mkdir -p $RPM_BUILD_ROOT%{_sbindir}
#mv $RPM_BUILD_ROOT%{_bindir}/%{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}

# Stolen from guarddog spec
### consolehelper entry
#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
#ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/%{name}
#cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/%{name} <<EOF
#USER=root
#PROGRAM=%{_sbindir}/%{name}
#SESSION=true
#FALLBACK=true
#EOF

### pam entry
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/%{name} <<EOF
auth       sufficient   pam_rootok.so
auth       include	system-auth
session    optional     pam_xauth.so
account    required     pam_permit.so
EOF

%clean
rm -rf %buildroot

%post
%update_menus

%postun
%clean_menus

%files -f %{name}.lang
%defattr(0755,root,root,0755)
%{_bindir}/%{name}
%defattr(0644,root,root,0755)
%{_menudir}/%{name}
%{_datadir}/applnk/kvpnc.desktop

%dir %{_datadir}/apps/kvpnc/
%{_datadir}/apps/kvpnc/eventsrc
%{_datadir}/apps/kvpnc/kvpncui.rc
%{_datadir}/apps/kvpnc/ping_check.sh

%{_datadir}/icons/*/*/apps/*.png
%{_datadir}/apps/kvpnc/icons/*/*/actions/*.png
%{_datadir}/apps/kvpnc/icons/*/*/apps/*.png
%{_datadir}/apps/kvpnc/newprofilewizard.png
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
#%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%doc %_docdir/HTML/*/%{name}/*
%doc %_docdir/HTML/%{name}/*.txt
%doc %_docdir/HTML/kvpnc/update_handbook.sh
%doc %_docdir/HTML/kvpnc/README.handbook
%doc %_docdir/HTML/kvpnc/README.smartcard

%_datadir/apps/kvpnc/ovpn.protocol
%_datadir/apps/kvpnc/pcf.protocol


