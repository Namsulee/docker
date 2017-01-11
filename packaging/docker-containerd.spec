%define project_path /src/github.com/docker
%define go_version 1.7.3

Name: docker-containerd
Version: 1.12.2
Release: 0
Summary: Docker Containerd
Group: Tools/Docker

License: ASL 2.0
Source0: %{name}.tar.gz
Source1: %{name}.manifest
Source11: go1.7.3.linux-amd64.tar.gz
Source12: go1.7.3.linux-armv7.tar.gz

BuildRequires: git
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: docker-engine
Requires: docker-runc 

%description
Docker Containerd

%prep
%setup -q
mkdir -p .%project_path/containerd
mv `ls . | grep -v packaging | grep -v src` .%project_path/containerd

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

echo 'containerd build'
export CGO_ENABLED=1
cd containerd
make

%install
# install binary
install -d $RPM_BUILD_ROOT/%{_bindir}
# install containerd
install -p -m 755 .%project_path/containerd/bin/containerd $RPM_BUILD_ROOT/%{_bindir}/docker-containerd
install -p -m 755 .%project_path/containerd/bin/containerd-shim $RPM_BUILD_ROOT/%{_bindir}/docker-containerd-shim
install -p -m 755 .%project_path/containerd/bin/ctr $RPM_BUILD_ROOT/%{_bindir}/docker-containerd-ctr

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
/%{_bindir}/docker-containerd
/%{_bindir}/docker-containerd-shim
/%{_bindir}/docker-containerd-ctr
%license .%project_path/containerd/LICENSE.code

