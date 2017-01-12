%define project_path /src/github.com/docker
%define go_version 1.7.3
%define orig_version %{version}-rc3

Name: docker-engine
Version: 1.12.2
Release: 0
Summary: The open-source application container engine
Group: Tools/Docker

License: ASL 2.0
Source0: %{name}.tar.gz
Source1: %{name}.manifest
Source11: go1.7.3.linux-amd64.tar.gz
Source12: go1.7.3.linux-armv7.tar.gz

BuildRequires: git
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: docker-containerd
Requires: docker-runc 

%description
Docker is an open source project to build, ship and run any application as a
lightweight container.

Docker containers are both hardware-agnostic and platform-agnostic. This means
they can run anywhere, from your laptop to the largest EC2 compute instance and
everything in between - and they don't require you to use a particular
language, framework or packaging system. That makes them great building blocks
for deploying and scaling web apps, databases, and backend services without
depending on a particular stack or provider.


%prep
%setup -q
mkdir -p .%project_path/
mv `ls . | grep -v packaging | grep -v src` .%project_path

%ifarch armv7l
cp %{SOURCE12} .
tar -zxf %{SOURCE12}
rm -f %{_builddir}/%{name}-%{version}/go%{go_version}.linux-armv7.tar.gz
%endif
%ifarch x86_64
cp %{SOURCE11} .
tar -zxf %{SOURCE11}
rm -f %{_builddir}/%{name}-%{version}/go%{go_version}.linux-amd64.tar.gz
%endif
chmod g-w %_sourcedir/*
cp %{SOURCE1} ./%{name}.manifest

%build
cd .%project_path
export GOROOT=%{_builddir}/%{name}-%{version}/go
export PATH=$PATH:%{_builddir}/%{name}-%{version}/go/bin
export GOPATH=%{_builddir}/%{name}-%{version}
export DOCKER_BUILDTAGS='exclude_graphdriver_btrfs exclude_graphdriver_devicemapper'

go env
echo 'docker, dockerd'
export CGO_ENABLED=1
AUTO_GOPATH=1 ./hack/make.sh dynbinary

%install
# install binary
install -d $RPM_BUILD_ROOT/%{_bindir}
# install containerd
install -p -m 755 .%project_path/bundles/%{orig_version}/dynbinary-client/docker-%{orig_version} $RPM_BUILD_ROOT/%{_bindir}/docker
install -p -m 755 .%project_path/bundles/%{orig_version}/dynbinary-daemon/dockerd-%{orig_version} $RPM_BUILD_ROOT/%{_bindir}/dockerd
install -p -m 755 .%project_path/bundles/%{orig_version}/dynbinary-daemon/docker-proxy-%{orig_version} $RPM_BUILD_ROOT/%{_bindir}/docker-proxy

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
/%{_bindir}/docker
/%{_bindir}/dockerd
/%{_bindir}/docker-proxy
%license .%project_path/LICENSE

