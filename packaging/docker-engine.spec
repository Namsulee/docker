%define __os_install_post %{nil}
%define __strip /bin/true
%define __spec_install_post %{nil}
%define _origversion %{version}

Name: docker-engine
Version: 1.12.5
Release: 0
Summary: The open-source application container engine
Group: Tools/Docker

License: ASL 2.0
Source0: %{name}.tar.gz
Source1: %{name}.manifest
Source2: docker.tar.gz
URL: https://dockerproject.org

BuildRequires: git
BuildRequires: golang
BuildRequires: python, libcurl-devel
BuildRequires: iptables
Requires(postun): /sbin/ldconfig
Requires(post): /sbin/ldconfig
# required packages on install
# conflicting packages
Conflicts: docker
Conflicts: docker-io
Conflicts: docker-engine-cs

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
%setup -n %{name}
chmod g-w %_sourcedir/*
cp %{SOURCE1} ./%{name}.manifest
cp %{SOURCE2} .
mkdir -p ./src/github.com/
tar -zxf %{SOURCE2} -C ./src/github.com/

%build
export GOROOT=/usr/local/go
export PATH=$PATH:/usr/local/go/bin
export GOPATH=%{_builddir}/%{name}
export DOCKER_BUILDTAGS='exclude_graphdriver_btrfs exclude_graphdriver_devicemapper'
%ifarch armv7l
export GOOS=linux GOARCH=arm GOARM=7
%endif

%ifarch aarch64
export GOOS=linux GOARCH=arm64 GOARM=
%endif

%ifarch x86_64
export GOOS=linux GOARCH=amd64 GOARM=
%endif

#export CGO_ENABLED=0
cd src/github.com/docker
export AUTO_GOPATH=1 
export CGO_ENABLED=0
export GOGCCFLAGS=+lpthread, ldl, lc
./hack/make.sh binary

#Containerd
#echo 'containerd build'
#export CGO_ENABLED=0
#cd containerd
#make static
#cd ../../
#runc
#echo 'runc build'

#cd opencontainers/runc
#export CGO_ENABLED=1
#make static BUILDTAGS=""
#cp runc ../../docker
#cd ../../docker

%install
# install binary
#install -d $RPM_BUILD_ROOT/%{_bindir}
#cd src/github.com/docker
#install -p -m 755 bundles/%{_origversion}/binary-client/docker-%{_origversion} $RPM_BUILD_ROOT/%{_bindir}/docker
#install -p -m 755 bundles/%{_origversion}/binary-daemon/dockerd-%{_origversion} $RPM_BUILD_ROOT/%{_bindir}/dockerd
#install -p -m 755 bundles/%{_origversion}/binary-daemon/docker-proxy-%{_origversion} $RPM_BUILD_ROOT/%{_bindir}/docker-proxy

# install containerd
#install -p -m 755 containerd/bin/containerd $RPM_BUILD_ROOT/%{_bindir}/docker-containerd
#install -p -m 755 containerd/bin/containerd-shim $RPM_BUILD_ROOT/%{_bindir}/docker-containerd-shim
#install -p -m 755 containerd/bin/ctr $RPM_BUILD_ROOT/%{_bindir}/docker-containerd-ctr

# install runc
#install -p -m 755 runc $RPM_BUILD_ROOT/%{_bindir}/docker-runc

# install udev rules
#install -d $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d
#install -p -m 644 contrib/udev/80-docker.rules $RPM_BUILD_ROOT/%{_sysconfdir}/udev/rules.d/80-docker.rules

# add init scripts
#install -d $RPM_BUILD_ROOT/etc/sysconfig
#install -d $RPM_BUILD_ROOT/%{_initddir}


#install -d $RPM_BUILD_ROOT/%{_unitdir}
#install -p -m 644 contrib/init/systemd/docker.service.rpm $RPM_BUILD_ROOT/%{_unitdir}/docker.service
# add bash, zsh, and fish completions
#install -d $RPM_BUILD_ROOT/usr/share/bash-completion/completions
#install -d $RPM_BUILD_ROOT/usr/share/zsh/vendor-completions
#install -d $RPM_BUILD_ROOT/usr/share/fish/vendor_completions.d
#install -p -m 644 contrib/completion/bash/docker $RPM_BUILD_ROOT/usr/share/bash-completion/completions/docker
#install -p -m 644 contrib/completion/zsh/_docker $RPM_BUILD_ROOT/usr/share/zsh/vendor-completions/_docker
#install -p -m 644 contrib/completion/fish/docker.fish $RPM_BUILD_ROOT/usr/share/fish/vendor_completions.d/docker.fish

%files
#/%{_bindir}/docker
#/%{_bindir}/dockerd
#/%{_bindir}/docker-containerd
#/%{_bindir}/docker-containerd-shim
#/%{_bindir}/docker-containerd-ctr
#/%{_bindir}/docker-proxy
#/%{_bindir}/docker-runc
#/%{_sysconfdir}/udev/rules.d/80-docker.rules
#/%{_unitdir}/docker.service
#%license LICENSE
#/usr/share/bash-completion/completions/docker
#/usr/share/zsh/vendor-completions/_docker
#/usr/share/fish/vendor_completions.d/docker.fish


%post
#%systemd_post docker
#if ! getent group docker > /dev/null; then
#    groupadd --system docker
#fi

%preun
#%systemd_preun docker

%postun
#%systemd_postun_with_restart docker

