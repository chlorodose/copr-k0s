Name:           k0s-policy
Version:        1.0.0
Release:        %autorelease
Summary:        SELinux Policy for k0s
License:        Apache-2.0

BuildArch:      noarch
Requires:       container-selinux
BuildRequires:  selinux-policy-devel
Requires:       selinux-policy-base, policycoreutils, libselinux-utils

Source0:        k0s.fc
Source1:        k0s.te

%description
This package installs and sets up the SELinux policy security module for k0s.

%prep
cp %{SOURCE0} k0s.fc
cp %{SOURCE1} k0s.te

%build
make -f /usr/share/selinux/devel/Makefile k0s.pp

%install
install -vd                 %{buildroot}%{_datadir}/selinux/packages
install -m 644 -vp k0s.pp   %{buildroot}%{_datadir}/selinux/packages/k0s.pp

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/k0s.pp

%pre
%selinux_relabel_pre

%posttrans
%selinux_relabel_post

%post
%selinux_modules_install %{_datadir}/selinux/packages/k0s.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    for P in /{etc,opt}/cni /var/lib/k0s/{bin,containerd}; do
        if [ -e "$P" ]; then
            restorecon -R "$P"
        fi
    done
fi;

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall k0s
fi;

%autochangelog
