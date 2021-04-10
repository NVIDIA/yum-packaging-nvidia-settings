# yum packaging nvidia settings

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Contributing](https://img.shields.io/badge/Contributing-Developer%20Certificate%20of%20Origin-violet)](https://developercertificate.org)

## Overview

Packaging templates for `yum` and `dnf` based Linux distros to build NVIDIA settings packages.

The `main` branch contains this README. The `.spec` and `.patch` files can be found in the appropriate [rhel7](../../tree/rhel7), [rhel8](../../tree/rhel8), and [fedora](../../tree/fedora) branches.

## Table of Contents

- [Overview](#Overview)
- [Deliverables](#Deliverables)
- [Prerequisites](#Prerequisites)
  * [Clone this git repository](#Clone-this-git-repository)
  * [Install build dependencies](#Install-build-dependencies)
- [Building with script](#Building-with-script)
- [Building Manually](#Building-Manually)
- [Related](#Related)
  * [DKMS nvidia](#DKMS-nvidia)
  * [NVIDIA driver](#NVIDIA-driver)
  * [NVIDIA kmod common](#NVIDIA-kmod-common)
  * [NVIDIA modprobe](#NVIDIA-modprobe)
  * [NVIDIA persistenced](#NVIDIA-persistenced)
  * [NVIDIA plugin](#NVIDIA-plugin)
  * [NVIDIA precompiled kmod](#NVIDIA-precompiled-kmod)
  * [NVIDIA xconfig](#NVIDIA-xconfig)
- [Contributing](#Contributing)


## Deliverables

This repo contains the `.spec` file used to build the following **RPM** packages:


> _note:_ `XXX` is the first `.` delimited field in the driver version, ex: `460` in `460.32.03`

* **RHEL8** or **Fedora** streams: `XXX`, `XXX-dkms`, `latest`, and `latest-dkms`
 ```shell
 - nvidia-libXNVCtrl
 - nvidia-libXNVCtrl-devel
 - nvidia-settings
 ```


For RHEL7 and derivatives, there are three sets or flavors of packages with different package dependencies. However, that does not apply to the packages in this repository.

* **RHEL7** flavor: `branch-XXX`, `latest`, and `latest-dkms`
 ```shell
 - nvidia-libXNVCtrl
 - nvidia-libXNVCtrl-devel
 - nvidia-settings
 ```


## Prerequisites

### Clone this git repository:

Supported branches: `rhel7`, `rhel8` & `fedora`

```shell
git clone -b ${branch} https://github.com/NVIDIA/yum-packaging-nvidia-settings
> ex: git clone -b rhel8 https://github.com/NVIDIA/yum-packaging-nvidia-settings
```

### Download a NVIDIA settings tarball:

* **Source code** location: [https://github.com/NVIDIA/nvidia-settings/releases](https://github.com/NVIDIA/nvidia-settings/releases)

  *ex:* [https://github.com/NVIDIA/nvidia-settings/archive/460.32.03.tar.gz](https://github.com/NVIDIA/nvidia-settings/archive/460.32.03.tar.gz)

  *ex:* [https://github.com/NVIDIA/nvidia-settings/archive/460.56.tar.gz](https://github.com/NVIDIA/nvidia-settings/archive/460.56.tar.gz)

### Install build dependencies

```shell
# Basics
yum install gcc m4
# Compiling UI
yum install gtk2-devel gtk3-devel libappstream-glib
# X.org utilties
yum install libXext-devel libXrandr-devel
# GLVND
yum install mesa-libGL-devel mesa-libEGL-devel
# Video extensions
yum install libXxf86vm-devel libXv-devel libvdpau-devel
# Misc
yum install jansson-devel dbus-devel desktop-file-utils
# Packaging
yum install rpm-build
```

## Building with script

### Fetch script from `main` branch

```shell
cd yum-packaging-nvidia-persistenced
git checkout remotes/origin/main -- build.sh
```

### Usage

```shell
./build.sh [$version | path/to/*.tar.{gz,bz2} | path/to/*.run]
> ex: time ./build.sh 460.32.03
> ex: time ./build.sh ~/Downloads/nvidia-settings-450.102.04.tar.bz2
> ex: time ./build.sh ~/Downloads/nvidia-settings-460.32.03.tar.gz
> ex: time ./build.sh ~/Downloads/NVIDIA-Linux-x86_64-450.102.04.run
```
> _note:_ runfile is only used to determine version


## Building Manually

### Packaging

```shell
mkdir BUILD BUILDROOT RPMS SRPMS SOURCES SPECS
cp *.desktop SOURCES/
cp *.patch SOURCES/
cp *.xml SOURCES/
cp nvidia-settings-${version}.tar.gz SOURCES/
cp nvidia-settings.spec SPECS/

rpmbuild \
    --define "%_topdir $(pwd)" \
    --define "debug_package %{nil}" \
    --define "version $version" \
    --define "epoch 3" \
    --define "extension gz" \
    -v -bb SPECS/nvidia-settings.spec
```
> _note:_ this package is not branched, therefore regardless of flavor, the highest version installed by default.

## Related

### DKMS nvidia

- dkms-nvidia
  * [https://github.com/NVIDIA/yum-packaging-dkms-nvidia](https://github.com/NVIDIA/yum-packaging-dkms-nvidia)

### NVIDIA driver

- nvidia-driver
  * [https://github.com/NVIDIA/yum-packaging-nvidia-driver](https://github.com/NVIDIA/yum-packaging-nvidia-driver)

### NVIDIA kmod common

- Common files
  * [https://github.com/NVIDIA/yum-packaging-nvidia-kmod-common](https://github.com/NVIDIA/yum-packaging-nvidia-kmod-common)

### NVIDIA modprobe

- nvidia-modprobe
  * [https://github.com/NVIDIA/yum-packaging-nvidia-modprobe](https://github.com/NVIDIA/yum-packaging-nvidia-modprobe)

### NVIDIA persistenced

- nvidia-persistenced
  * [https://github.com/NVIDIA/yum-packaging-nvidia-persistenced](https://github.com/NVIDIA/yum-packaging-nvidia-persistenced)

### NVIDIA plugin

- _dnf-plugin-nvidia_ & _yum-plugin-nvidia_
  * [https://github.com/NVIDIA/yum-packaging-nvidia-plugin](https://github.com/NVIDIA/yum-packaging-nvidia-plugin)

### NVIDIA precompiled kmod

- Precompiled kernel modules
  * [https://github.com/NVIDIA/yum-packaging-precompiled-kmod](https://github.com/NVIDIA/yum-packaging-precompiled-kmod)

### NVIDIA xconfig

- nvidia-xconfig
  * [https://github.com/NVIDIA/yum-packaging-nvidia-xconfig](https://github.com/NVIDIA/yum-packaging-nvidia-xconfig)


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
