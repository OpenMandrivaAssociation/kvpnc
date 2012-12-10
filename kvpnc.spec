%define name    kvpnc
%define version 0.9.6a
%define rel     1
%define release %mkrel %rel
%define Summary KDE frontend to various vpn clients

Summary:        %{Summary}
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        GPLv2+
Group:          Networking/Remote access
Source0:        http://download.gna.org/kvpnc/kvpnc-%{version}-kde4.tar.bz2
URL:            http://home.gna.org/kvpnc/en/index.html
Patch0:		kvpnc-0.9.6a-gcc47.patch
Patch1:		kvpnc-0.9.6a-scriptsec.patch
BuildRequires:  desktop-file-utils
BuildRequires:  kdelibs4-devel
BuildRequires:  libgcrypt-devel
Requires:       usermode-consoleonly
Requires:       kvpnc-backend

%description
KVpnc is a KDE frontend for for various vpn clients.
It supports Cisco VPN (vpnc) and IPSec (FreeS/WAN, racoon).
Vpnc is a replacement for the cisco VPN client and its used 
as client for the cisco3000 VPN Concentrator, FreeS/WAN (OpenS/WAN) 
is a IPSec client for Linux 2.4.x and racoon is a IPSec client 
for Linux 2.6.x and *BSD.

%files 
%{_kde_bindir}/%{name}
%{_kde_datadir}/applications/kde4/kvpnc.desktop
%{_kde_datadir}/apps/kvpnc
%{_kde_datadir}/icons/*/*/apps/*.png
%{_kde_datadir}/icons/*/*/actions/*.png
%config(noreplace) %{_sysconfdir}/pam.d/%{name}

#--------------------------------------------------------------------

%prep
%setup -q -n kvpnc-%{version}-kde4
%patch0 -p1
%patch1 -p1

%build
%cmake_kde4
%make
cd ..

%install
%makeinstall_std -C build

### pam entry
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/%{name} <<EOF
auth       sufficient   pam_rootok.so
auth       include      system-auth
session    optional     pam_xauth.so
account    required     pam_permit.so
EOF
