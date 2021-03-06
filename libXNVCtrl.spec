%define  oname libXNVCtrl
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

Name:           XNVCtrl
Version:        440.82
Release:        2
Summary:        Library providing the NV-CONTROL API
License:        GPLv2+
URL:            https://download.nvidia.com/XFree86/nvidia-settings/
Source0:        %{url}/nvidia-settings-%{version}.tar.bz2
Patch0:         libxnvctrl_so_0.patch

#BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xext)
BuildRequires: hostname

%description
This packages contains the libXNVCtrl library from the nvidia-settings
application. This library provides the NV-CONTROL API for communicating with
the proprietary NVidia xorg driver. This package does not contain the
nvidia-settings tool itself as that is included with the proprietary drivers
themselves. 

%package -n %{libname}
Summary:	Library providing the NV-CONTROL API
Provides: nvidia-%{oname} = 3:%{version}-100

%description -n %{libname}
This packages contains the libXNVCtrl library from the nvidia-settings
application. This library provides the NV-CONTROL API for communicating with
the proprietary NVidia xorg driver. This package does not contain the
nvidia-settings tool itself as that is included with the proprietary drivers
themselves. 

%package -n %{devname}
Summary:        Development files for %{name}
Requires:       %{libname}%{?_isa} = %{version}-%{release}
Requires:       %{_lib}xext-devel

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n nvidia-settings-%{version}


%build
%{set_build_flags}
%make_build \
   CC="%{__cc}" \
   NV_VERBOSE=1 \
   DO_STRIP=0 \
   STRIP_CMD=/dev/true \
   -C src/%{oname} \
   libXNVCtrl.so


%install
pushd src/%{oname}
install -m 0755 -d $RPM_BUILD_ROOT%{_libdir}/
install -p -m 0755 libXNVCtrl.so.0.0.0    $RPM_BUILD_ROOT%{_libdir}/
ln -s libXNVCtrl.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/libXNVCtrl.so.0
ln -s libXNVCtrl.so.0 $RPM_BUILD_ROOT%{_libdir}/libXNVCtrl.so
install -m 0755 -d $RPM_BUILD_ROOT%{_includedir}/NVCtrl/
install -p -m 0644 {nv_control,NVCtrl,NVCtrlLib}.h $RPM_BUILD_ROOT%{_includedir}/NVCtrl/
popd


%files -n %{libname}
%license COPYING
%{_libdir}/%{oname}.so.0*

%files -n %{devname}
%doc doc/NV-CONTROL-API.txt doc/FRAMELOCK.txt
%{_includedir}/NVCtrl
%{_libdir}/%{oname}.so
