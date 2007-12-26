%define name    kvpnc
%define version 0.9.0
%define rel     1
%define release %mkrel %rel
%define Summary KDE frontend to various vpn clients

%define unstable 1
%define use_enable_final 1

Summary:        %{Summary}
Name:           %{name}
Version:        %{version}
Release:        %{release}
License: 	GPLv2+
Group: 		Graphical desktop/KDE
Source: 	http://download.gna.org/kvpnc/kvpnc-%{version}.tar.bz2
URL: 		http://home.gna.org/kvpnc/en/index.html
BuildRequires:	desktop-file-utils
BuildRequires: 	kdelibs-devel
BuildRequires:  libgcrypt-devel
Requires: 	usermode-consoleonly
Requires: 	kvpnc-backend


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

%configure2_5x --disable-rpath \
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
%makeinstall_std

desktop-file-install --delete-original --vendor='' \
	--dir %buildroot%_datadir/applications/kde \
	%buildroot%_datadir/applnk/*.desktop

%find_lang %{name} --with-html

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
%{_datadir}/applications/kde/kvpnc.desktop
%{_datadir}/apps/kvpnc
%{_datadir}/icons/*/*/apps/*.png
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
#%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%_datadir/doc/HTML/kvpnc
%_datadir/apps/kvpnc/ovpn.protocol
%_datadir/apps/kvpnc/pcf.protocol


