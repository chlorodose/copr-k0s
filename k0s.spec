%global tag             1.35.1
%global debug_package   %{nil}
%global __os_install_post %{nil}

Name:           k0s
Release:        %autorelease
Version:        %{tag}
Summary:        Zero Friction Kubernetes

License:        Apache-2.0
URL:            https://k0sproject.io/
Source0:        args.env
Source1:        k0s.service
Source10:       https://github.com/k0sproject/k0s/releases/download/v%{tag}%2Bk0s.1/k0s-v%{tag}+k0s.1-amd64
Source11:       https://github.com/k0sproject/k0s/releases/download/v%{tag}%2Bk0s.1/k0s-v%{tag}+k0s.1-arm64
Source20:       https://github.com/k0sproject/k0s/releases/download/v%{tag}%2Bk0s.1/sha256sums.txt
ExclusiveArch:  x86_64 arm64

Requires:       systemd
Recommends:     k0s-policy

%prep
cp %{SOURCE10} %{SOURCE11} .
sha256sum --ignore-missing -c %{SOURCE20}

%description
k0s - The Zero Friction Kubernetes

%files
%{_bindir}/k0s
%{_bindir}/kubectl
%{_prefix}/lib/systemd/system/k0s.service
%dir %{_sysconfdir}/k0s
%config %attr(600, root, root) %{_sysconfdir}/k0s/args.env
%ghost %config %attr(600, root, root) %{_sysconfdir}/k0s/k0s.yaml

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
%ifarch x86_64
install -m 0755 -vp %{S:10}             %{buildroot}%{_bindir}/k0s
%endif
%ifarch aarch64
install -m 0755 -vp %{S:11}             %{buildroot}%{_bindir}/k0s
%endif
ln -sf k0s                              %{buildroot}%{_bindir}/kubectl
install -m 0755 -vd                     %{buildroot}%{_sysconfdir}/k0s
install -m 0600 -vp %{S:0}              %{buildroot}%{_sysconfdir}/k0s/args.env
install -m 0755 -vd                     %{buildroot}%{_prefix}/lib/systemd/system/
install -m 0644 -vp %{S:1}              %{buildroot}%{_prefix}/lib/systemd/system/k0s.service

%post
%systemd_post k0s.target
%systemd_post k0s-master.target
%systemd_post k0s-controller.target
%systemd_post k0s-worker.target
k0s config create >%{_sysconfdir}/k0s/k0s.yaml || true

%postun
%systemd_post k0s.target
%systemd_post k0s-master.target
%systemd_post k0s-controller.target
%systemd_post k0s-worker.target

%changelog
%autochangelog
