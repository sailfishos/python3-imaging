%define py_incdir %{_includedir}/python%{python3_version}

Summary:       Python's own image processing library
Name:          python3-imaging
Version:       12.2.0
Release:       1
License:       BSD
URL:           https://github.com/sailfishos/python3-imaging
Source0:       %{name}-%{version}.tar.gz
Patch1:        0001-Revert-Add-parallel-compile-from-pybind11.patch
Patch2:        0002-Revert-Replace-deprecated-classifier-with-licence-ex.patch

BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(zlib)
BuildRequires: python3-setuptools

%description
Python Imaging Library

The Python Imaging Library (PIL) adds image processing capabilities
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

Notice that in order to reduce the package dependencies there are
three subpackages: devel (for development); tk (to interact with the
tk interface) and sane (scanning devices interface).

%package devel
Summary: Development files for python-imaging
Requires: %{name} = %{version}-%{release}, python3-devel
Requires: pkgconfig(libjpeg)
Requires: pkgconfig(zlib)

%description devel
Development files for python-imaging.

%prep
%autosetup -p1 -n %{name}-%{version}/Pillow

%build
%py3_build

%install
mkdir -p %{buildroot}%{py_incdir}/Imaging
install -m 644 src/libImaging/*.h %{buildroot}%{py_incdir}/Imaging
%py3_install

# There is no need to ship the binaries since they are already packaged
# in %doc
rm -rf %{buildroot}%{_bindir}

%check
PYTHONPATH=$(ls -1d build/lib.linux*) %{__python3} selftest.py --installed

%files
%license docs/COPYING
%dir %{python3_sitearch}/PIL
%{python3_sitearch}/PIL/*
%{python3_sitearch}/*.egg-info

%files devel
%{py_incdir}/Imaging
