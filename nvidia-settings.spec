Name:           nvidia-settings
Version:        418.43
Release:        1%{?dist}
Summary:        Configure the NVIDIA graphics driver
Epoch:          3
License:        GPLv2+
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  %{ix86} x86_64

Source0:        https://download.nvidia.com/XFree86/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}-load.desktop
Source2:        %{name}.appdata.xml
Patch0:         %{name}-367.44-validate.patch
Patch1:         %{name}-375.10-defaults.patch
Patch2:         %{name}-410.57-libXNVCtrl-so.patch

BuildRequires:  desktop-file-utils
BuildRequires:  dbus-devel
BuildRequires:  gcc
BuildRequires:  gtk2-devel > 2.4
BuildRequires:  jansson-devel
BuildRequires:  libvdpau-devel >= 1.0
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  m4
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  gtk3-devel
%endif

Requires:       nvidia-libXNVCtrl%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       nvidia-driver%{?_isa} = %{?epoch}:%{version}
# Loaded at runtime
Requires:       libvdpau%{?_isa} >= 0.9

Obsoletes:      nvidia-settings-desktop < %{?epoch}:%{version}-%{release}

%description
The %{name} utility is a tool for configuring the NVIDIA graphics
driver. It operates by communicating with the NVIDIA X driver, querying and
updating state as appropriate.

This communication is done with the NV-CONTROL X extension.

%package -n nvidia-libXNVCtrl
Summary:        Library providing the NV-CONTROL API
Obsoletes:      libXNVCtrl < %{?epoch}:%{version}-%{release}
Provides:       libXNVCtrl = %{?epoch}:%{version}-%{release}

%description -n nvidia-libXNVCtrl
This library provides the NV-CONTROL API for communicating with the proprietary
NVidia xorg driver. It is required for proper operation of the %{name} utility.

%package -n nvidia-libXNVCtrl-devel
Summary:        Development files for libXNVCtrl
Requires:       nvidia-libXNVCtrl = %{?epoch}:%{version}-%{release}
Requires:       libX11-devel

%description -n nvidia-libXNVCtrl-devel
This devel package contains libraries and header files for
developing applications that use the NV-CONTROL API.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Remove bundled jansson
rm -fr src/jansson

# Remove additional CFLAGS added when enabling DEBUG
sed -i '/+= -O0 -g/d' utils.mk src/libXNVCtrl/utils.mk

# Change all occurrences of destinations in each utils.mk.
sed -i -e 's|$(PREFIX)/lib|$(PREFIX)/%{_lib}|g' utils.mk src/libXNVCtrl/utils.mk

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"
make %{?_smp_mflags} \
    DEBUG=1 \
    NV_USE_BUNDLED_LIBJANSSON=0 \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \

%install
# Install libXNVCtrl headers
mkdir -p %{buildroot}%{_includedir}/NVCtrl
cp -af src/libXNVCtrl/*.h %{buildroot}%{_includedir}/NVCtrl/

# Install main program
%make_install \
    DEBUG=1 \
    NV_USE_BUNDLED_LIBJANSSON=0 \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix}


# Install desktop file
mkdir -p %{buildroot}%{_datadir}/{applications,pixmaps}
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ doc/%{name}.desktop
cp doc/%{name}.png %{buildroot}%{_datadir}/pixmaps/
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# Install autostart file to load settings at login
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-load.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-load.desktop

%if 0%{?fedora}
# install AppData and add modalias provides
mkdir -p %{buildroot}%{_datadir}/appdata
install -p -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/appdata/
%endif

%post -n nvidia-libXNVCtrl -p /sbin/ldconfig

%postun -n nvidia-libXNVCtrl -p /sbin/ldconfig

%post
/sbin/ldconfig
%if 0%{?rhel} == 7
/usr/bin/update-desktop-database &> /dev/null || :
%endif

%postun
/sbin/ldconfig
%if 0%{?rhel} == 7
/usr/bin/update-desktop-database &> /dev/null || :
%endif

%files
%{_bindir}/%{name}
%if 0%{?fedora}
%{_datadir}/appdata/%{name}.appdata.xml
%endif
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_libdir}/libnvidia-gtk*.so.%{version}
%{_mandir}/man1/%{name}.*
%{_sysconfdir}/xdg/autostart/%{name}-load.desktop

%files -n nvidia-libXNVCtrl
%license COPYING
%{_libdir}/libXNVCtrl.so.*

%files -n nvidia-libXNVCtrl-devel
%doc doc/NV-CONTROL-API.txt doc/FRAMELOCK.txt
%{_includedir}/NVCtrl
%{_libdir}/libXNVCtrl.so

%changelog
* Fri Feb 22 2019 Simone Caronni <negativo17@gmail.com> - 3:418.43-1
- Update to 418.43.
- Trim changelog.

* Wed Feb 06 2019 Simone Caronni <negativo17@gmail.com> - 3:418.30-1
- Update to 418.30.

* Thu Jan 17 2019 Simone Caronni <negativo17@gmail.com> - 3:415.27-1
- Update to 415.27.

* Thu Dec 20 2018 Simone Caronni <negativo17@gmail.com> - 3:415.25-1
- Update to 415.25.

* Fri Dec 14 2018 Simone Caronni <negativo17@gmail.com> - 3:415.23-1
- Update to 415.23.

* Sun Dec 09 2018 Simone Caronni <negativo17@gmail.com> - 3:415.22-1
- Update to 415.22.

* Thu Nov 22 2018 Simone Caronni <negativo17@gmail.com> - 3:415.18-1
- Update to 415.18.

* Mon Nov 19 2018 Simone Caronni <negativo17@gmail.com> - 3:410.78-1
- Update to 410.78.

* Fri Oct 26 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-1
- Update to 410.73.

* Wed Oct 17 2018 Simone Caronni <negativo17@gmail.com> - 3:410.66-1
- Update to 410.66.

* Sat Sep 22 2018 Simone Caronni <negativo17@gmail.com> - 3:410.57-1
- Update to 410.57.

* Wed Aug 22 2018 Simone Caronni <negativo17@gmail.com> - 3:396.54-1
- Update to 396.54.

* Sun Aug 19 2018 Simone Caronni <negativo17@gmail.com> - 3:396.51-1
- Update to 396.51.

* Fri Jul 20 2018 Simone Caronni <negativo17@gmail.com> - 3:396.45-1
- Update to 396.45.

* Fri Jun 01 2018 Simone Caronni <negativo17@gmail.com> - 3:396.24-1
- Update to 396.24.

* Tue May 22 2018 Simone Caronni <negativo17@gmail.com> - 3:390.59-1
- Update to 390.59.

* Tue Apr 03 2018 Simone Caronni <negativo17@gmail.com> - 3:390.48-1
- Update to 390.48.

* Thu Mar 15 2018 Simone Caronni <negativo17@gmail.com> - 3:390.42-1
- Update to 390.42.

* Tue Feb 27 2018 Simone Caronni <negativo17@gmail.com> - 3:390.25-2
- Align Epoch with other components.

* Tue Jan 30 2018 Simone Caronni <negativo17@gmail.com> - 2:390.25-1
- Update to 390.25.

* Fri Jan 19 2018 Simone Caronni <negativo17@gmail.com> - 2:390.12-1
- Update to 390.12.
