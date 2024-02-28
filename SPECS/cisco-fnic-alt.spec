%define vendor_name Cisco
%define vendor_label cisco
%define driver_name fnic

# XCP-ng: install to the override directory
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 2.0.0.90
Release: 1%{?dist}
License: GPL

# Extracted from latest XS driver disk
Source0: cisco-fnic-2.0.0.90.tar.gz
Patch0: xcpng8-configure.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{vendor_label}-%{driver_name}-%{version}

%build
chmod +x configure
chmod +x version.sh
export KNAME=%{kernel_version}
./configure
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Wed Feb 28 2024 Gael Duperrey <gduperrey@vates.fr> - 2.0.0.90-1
- Update to version 2.0.0.90
- Synced from XS driver SRPM cisco-fnic-2.0.0.90-1.xs8~2_1.src.rpm

* Fri May 12 2023 Gael Duperrey <gduperrey@vates.fr> - 2.0.0.89-1
- Update to version 2.0.0.89

* Mon Nov 28 2022 Gael Duperrey <gduperrey@vates.fr> - 2.0.0.85-1
- initial package, version 2.0.0.85
