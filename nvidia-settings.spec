%global _basename nvidia-settings

%define _named_version %{driver_branch}

Name:           %{_basename}-%{_named_version}
Version:        410.73
Release:        1%{?dist}
Summary:        Configure the NVIDIA graphics driver
Epoch:          3
License:        GPLv2+
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  %{ix86} x86_64 ppc64le

Source0:        https://download.nvidia.com/XFree86/%{_basename}/%{_basename}-%{version}.tar.bz2
Source1:        %{_basename}-load.desktop
Source2:        %{_basename}.appdata.xml
Patch0:         %{_basename}-367.44-validate.patch
Patch1:         %{_basename}-375.10-defaults.patch
Patch2:         %{_basename}-410.57-libXNVCtrl-so.patch

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

Requires:       nvidia-libXNVCtrl-%{_named_version}%{?_isa} = %{?epoch}:%{version}
Requires:       nvidia-driver-%{_named_version}%{?_isa} = %{?epoch}:%{version}
# Loaded at runtime
Requires:       libvdpau%{?_isa} >= 0.9

%if 0%{?is_dkms} == 1
Obsoletes:      nvidia-settings-desktop < %{?epoch}:%{version}-%{release}
%endif

Provides:       %{_basename} = %{?epoch:%{epoch}:}%{version}-%{release}

%if 0%{?is_dkms} == 1
Obsoletes:      %{_basename} < %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description
The %{_basename} utility is a tool for configuring the NVIDIA graphics
driver. It operates by communicating with the NVIDIA X driver, querying and
updating state as appropriate.

This communication is done with the NV-CONTROL X extension.

%package -n nvidia-libXNVCtrl-%{_named_version}
Summary:        Library providing the NV-CONTROL API
Requires:       nvidia-driver-%{_named_version}%{?_isa} = %{?epoch}:%{version}

%if 0%{?is_dkms} == 1
Obsoletes:      libXNVCtrl < %{?epoch}:%{version}-%{release}
%endif

Provides:       libXNVCtrl = %{?epoch}:%{version}-%{release}
Provides:       nvidia-libXNVCtrl = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n nvidia-libXNVCtrl-%{_named_version}
This library provides the NV-CONTROL API for communicating with the proprietary
NVidia xorg driver. It is required for proper operation of the %{_basename} utility.

%package -n nvidia-libXNVCtrl-%{_named_version}-devel
Summary:        Development files for libXNVCtrl
Requires:       nvidia-driver-%{_named_version}%{?_isa} = %{?epoch}:%{version}
Requires:       nvidia-libXNVCtrl-%{_named_version} = %{?epoch}:%{version}
Requires:       libX11-devel
Provides:       nvidia-libXNVCtrl-devel = %{?epoch:%{epoch}:}%{version}

%description -n nvidia-libXNVCtrl-%{_named_version}-devel
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
export CFLAGS="%{optflags} -fPIC"
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
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ doc/%{_basename}.desktop
cp doc/%{_basename}.png %{buildroot}%{_datadir}/pixmaps/
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{_basename}.desktop

# Install autostart file to load settings at login
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/%{_basename}-load.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{_basename}-load.desktop

%if 0%{?fedora}
# install AppData and add modalias provides
mkdir -p %{buildroot}%{_datadir}/appdata
install -p -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/appdata/
%endif

%post -n nvidia-libXNVCtrl-%{_named_version} -p /sbin/ldconfig

%postun -n nvidia-libXNVCtrl-%{_named_version} -p /sbin/ldconfig

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
%{_bindir}/%{_basename}
%if 0%{?fedora}
%{_datadir}/appdata/%{_basename}.appdata.xml
%endif
%{_datadir}/applications/%{_basename}.desktop
%{_datadir}/pixmaps/%{_basename}.png
%{_libdir}/libnvidia-gtk*.so.%{version}
%{_mandir}/man1/%{_basename}.*
%{_sysconfdir}/xdg/autostart/%{_basename}-load.desktop

%files -n nvidia-libXNVCtrl-%{_named_version}
%if 0%{?rhel} == 6
%doc COPYING
%else
%license COPYING
%endif
%{_libdir}/libXNVCtrl.so.*

%files -n nvidia-libXNVCtrl-%{_named_version}-devel
%doc doc/NV-CONTROL-API.txt doc/FRAMELOCK.txt
%{_includedir}/NVCtrl
%{_libdir}/libXNVCtrl.so

%changelog
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

* Tue Nov 28 2017 Simone Caronni <negativo17@gmail.com> - 2:387.34-1
- Update to 387.34.

* Tue Oct 31 2017 Simone Caronni <negativo17@gmail.com> - 2:387.22-1
- Update to 387.22.

* Thu Oct 05 2017 Simone Caronni <negativo17@gmail.com> - 2:387.12-1
- Update to 387.12.

* Tue Oct 03 2017 Simone Caronni <negativo17@gmail.com> - 2:384.90-2
- Disable NVML experimental setting. Works only on some combination of cards and
  make the application just crash on others.

* Fri Sep 22 2017 Simone Caronni <negativo17@gmail.com> - 2:384.90-1
- Update to 384.90.

* Wed Aug 30 2017 Simone Caronni <negativo17@gmail.com> - 2:384.69-1
- Update to 384.69.
- Update SPEC file, set proper compiler flags on Fedora 27.

* Tue Jul 25 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-1
- Update to 384.59.

* Wed May 10 2017 Simone Caronni <negativo17@gmail.com> - 2:381.22-1
- Update to 381.22.

* Fri Apr 07 2017 Simone Caronni <negativo17@gmail.com> - 2:381.09-1
- Update to 381.09.

* Wed Feb 15 2017 Simone Caronni <negativo17@gmail.com> - 2:378.13-1
- Update to 378.13.

* Thu Jan 19 2017 Simone Caronni <negativo17@gmail.com> - 2:378.09-1
- Update to 378.09.

* Thu Dec 15 2016 Simone Caronni <negativo17@gmail.com> - 2:375.26-1
- Update to 375.26.

* Sat Nov 19 2016 Simone Caronni <negativo17@gmail.com> - 2:375.20-1
- Update to 375.20, switch to internal NVML header.
- Remove unused patches.

* Sat Oct 22 2016 Simone Caronni <negativo17@gmail.com> - 2:375.10-1
- Update to 375.10, NVML support now required.
- Specify to use system jansson also on install, or bundled copy is used.

* Fri Sep 09 2016 Simone Caronni <negativo17@gmail.com> - 2:370.28-1
- Update to 370.28.

* Wed Sep 07 2016 Simone Caronni <negativo17@gmail.com> - 2:370.23-3
- Update desktop file to latest spec for AppStream metadata.
- Add AppStream metadata file.

* Mon Sep 05 2016 Simone Caronni <negativo17@gmail.com> - 2:370.23-2
- Update requirements, make it require nvidia-driver.
- Add update-desktop-database to Fedora < 25 and RHEL/CentOS < 8.

* Wed Aug 17 2016 Simone Caronni <negativo17@gmail.com> - 2:370.23-1
- Update to 370.23.

* Fri Jul 22 2016 Simone Caronni <negativo17@gmail.com> - 2:367.35-1
- Update to 367.35.

* Mon Jun 13 2016 Simone Caronni <negativo17@gmail.com> - 2:367.27-1
- Update to 367.27.

* Thu May 26 2016 Simone Caronni <negativo17@gmail.com> - 2:367.18-1
- Update to 367.18.

* Mon May 02 2016 Simone Caronni <negativo17@gmail.com> - 2:364.19-1
- Update to 364.19.

* Fri Apr 08 2016 Simone Caronni <negativo17@gmail.com> - 2:364.15-1
- Update to 364.15.

* Tue Mar 22 2016 Simone Caronni <negativo17@gmail.com> - 2:364.12-1
- Update to 364.12.
- Update make parameters.

* Tue Feb 09 2016 Simone Caronni <negativo17@gmail.com> - 2:361.28-1
- Update to 361.28.

* Thu Jan 14 2016 Simone Caronni <negativo17@gmail.com> - 2:361.18-1
- Update to 361.18.

* Tue Jan 05 2016 Simone Caronni <negativo17@gmail.com> - 2:361.16-1
- Update to 361.16.
- Disable NVML.

* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 2:358.16-1
- Update to 358.16.

* Wed Nov 18 2015 Simone Caronni <negativo17@gmail.com> - 2:358.09-2
- Update isa requirements.

* Tue Oct 13 2015 Simone Caronni <negativo17@gmail.com> - 2:358.09-1
- Update to 358.09.

* Tue Sep 01 2015 Simone Caronni <negativo17@gmail.com> - 2:355.11-1
- Update to 355.11.

* Tue Aug 04 2015 Simone Caronni <negativo17@gmail.com> - 2:355.06-1
- Update to 355.06.
- Use Nvidia Management Library (GPU Deployment Kit).

* Wed Jul 29 2015 Simone Caronni <negativo17@gmail.com> - 2:352.30-1
- Update to 352.30.

* Wed Jun 17 2015 Simone Caronni <negativo17@gmail.com> - 2:352.21-1
- Update to 352.21.

* Tue May 19 2015 Simone Caronni <negativo17@gmail.com> - 2:352.09-1
- Update to 352.09.

* Wed May 13 2015 Simone Caronni <negativo17@gmail.com> - 2:346.72-1
- Update to 346.72.

* Tue Apr 07 2015 Simone Caronni <negativo17@gmail.com> - 2:346.59-1
- Update to 346.59.

* Wed Mar 11 2015 Simone Caronni <negativo17@gmail.com> - 2:346.47-2
- Require libvdpau >= 1.0 for h.265 support.

* Wed Feb 25 2015 Simone Caronni <negativo17@gmail.com> - 2:346.47-1
- Update to 346.47.
- Add license macro.

* Sat Jan 17 2015 Simone Caronni <negativo17@gmail.com> - 2:346.35-1
- Update to 346.35.
- Require libvdpau 0.9.

* Tue Dec 09 2014 Simone Caronni <negativo17@gmail.com> - 2:346.22-1
- Update to 346.22.

* Fri Nov 14 2014 Simone Caronni <negativo17@gmail.com> - 2:346.16-1
- Update to 346.16.
- Split previous patches in multiple patches, rework shared libXNVCTRL patch.
- Add new gtk2 and gtk3 libraries to package. This kills the gtk3 only package
  on Fedora and CentOS/RHEL 7. Sigh.

* Mon Sep 22 2014 Simone Caronni <negativo17@gmail.com> - 2:343.22-1
- Update to 343.22.

* Thu Aug 07 2014 Simone Caronni <negativo17@gmail.com> - 2:343.13-1
- Update to 343.13.
- Use GTK3 for RHEL 7+ and Fedora.

* Tue Jul 08 2014 Simone Caronni <negativo17@gmail.com> - 2:340.24-1
- Update to 340.24.

* Mon Jun 09 2014 Simone Caronni <negativo17@gmail.com> - 2:340.17-1
- Update to 340.17.
- Removed upstreamed patch.

* Tue Jun 03 2014 Simone Caronni <negativo17@gmail.com> - 2:337.25-2
- Fix requirements.

* Mon Jun 02 2014 Simone Caronni <negativo17@gmail.com> - 2:337.25-1
- Update to 337.25.

* Fri May 09 2014 Simone Caronni <negativo17@gmail.com> - 2:337.19-2
- Load settings at login.

* Tue May 06 2014 Simone Caronni <negativo17@gmail.com> - 2:337.19-1
- Update to 337.19.

* Tue Apr 08 2014 Simone Caronni <negativo17@gmail.com> - 2:337.12-1
- Update to 337.12.

* Tue Mar 04 2014 Simone Caronni <negativo17@gmail.com> - 2:334.21-1
- Update to 334.21.

* Wed Feb 19 2014 Simone Caronni <negativo17@gmail.com> - 2:331.49-1
- Update to 331.49.

* Tue Jan 14 2014 Simone Caronni <negativo17@gmail.com> - 2:331.38-1
- Update to 331.38.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-2
- Make libXNVCtrl an external library (adapted from Debian):
    Obsolete (useless) Fedora libXNVCtrl library.
    Make dynamic shared object optional at compile time.
    Version libXVNCtrl library according to driver version.
- Link libraries as needed, removing empty dependencies.
- Do not strip binaries during build, let rpm generate debuginfo files.

* Thu Nov 07 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-1
- Update to 331.20.

* Wed Oct 23 2013 Simone Caronni <negativo17@gmail.com> - 2:331.17-1
- Updated to 331.17.

* Fri Oct 04 2013 Simone Caronni <negativo17@gmail.com> - 2:331.13-1
- Update to 331.13.

* Mon Sep 09 2013 Simone Caronni <negativo17@gmail.com> - 2:325.15-1
- Update to 325.15.

* Wed Aug 07 2013 Simone Caronni <negativo17@gmail.com> - 2:319.49-1
- Updated to 319.49.

* Tue Jul 02 2013 Simone Caronni <negativo17@gmail.com> - 2:319.32-2
- Add armv7hl support.

* Fri Jun 28 2013 Simone Caronni <negativo17@gmail.com> - 1:319.32-1
- Update to 319.32.

* Fri May 24 2013 Simone Caronni <negativo17@gmail.com> - 1:319.23-2
- Add missing m4 build requirement.

* Fri May 24 2013 Simone Caronni <negativo17@gmail.com> - 1:319.23-1
- Update to 319.23.

* Thu May 02 2013 Simone Caronni <negativo17@gmail.com> - 1:319.17-1
- Update to 319.17.
- Switch to ftp://download.nvidia.com/ sources.

* Mon Apr 22 2013 Simone Caronni <negativo17@gmail.com> - 1:319.12-2
- Obsoletes nvidia-settings.desktop.

* Wed Apr 10 2013 Simone Caronni <negativo17@gmail.com> - 1:319.12-1
- Started off from rpmfusion-nonfree packages.
- Updated to 319.12.
- Add libvdpau BuildRequires.
- Simplify spec file; move version to official version; drop 1.0.
- Remove split desktop package; simplify packaging.
