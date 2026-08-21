%define vendor_name Cisco
%define vendor_label cisco
%define driver_name fnic

# XCP-ng: install to the override directory
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 2.0.0.89
Release: 2%{?dist}
# Built against new kABI after cip rebase
Requires: xcpng-kernel-kabi = 4.19.325-cip134+

License: GPL

# Extracted from latest XS driver disk
Source0: cisco-fnic-2.0.0.89.tar.gz

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
* Mon Aug 31 2026 Quentin Casasnovas <quentin.casasnovas@vates.tech> - 2.0.0.89-2
- Rebuild for kernel v4.19.325-cip134

* Fri May 12 2023 Gael Duperrey <gduperrey@vates.fr> - 2.0.0.89-1
- Update to version 2.0.0.89

* Mon Nov 28 2022 Gael Duperrey <gduperrey@vates.fr> - 2.0.0.85-1
- initial package, version 2.0.0.85
