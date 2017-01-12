%define project_path /src/github.com/opencontainers
%define go_version 1.7.3

Name: docker-runc
Version: 1.0.0
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
Requires: docker-engine
Requires: docker-containerd

%description
Runc is a CLI tool for spawning and running containers according to the OCI specification

%prep
%setup -q
mkdir -p .%project_path/runc
mv `ls . | grep -v packaging | grep -v src` .%project_path/runc

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
cd .%project_path/runc
export GOROOT=%{_builddir}/%{name}-%{version}/go
export PATH=$PATH:%{_builddir}/%{name}-%{version}/go/bin
export GOPATH=%{_builddir}/%{name}-%{version}

go env
echo 'runc'
make all BUILDTAGS=""
%install
# install binary
install -d $RPM_BUILD_ROOT/%{_bindir}
# install runc
install -p -m 755 .%project_path/runc/runc $RPM_BUILD_ROOT/%{_bindir}/docker-runc

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
/%{_bindir}/docker-runc
%license .%project_path/runc/LICENSE

