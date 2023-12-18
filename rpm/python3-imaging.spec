%define py_incdir %{_includedir}/python%{python3_version}

Summary:       Python's own image processing library
Name:          python3-imaging
Version:       9.0.0
Release:       1
License:       BSD
Source0:       %{name}-%{version}.tar.gz
URL:           https://python-pillow.org/

BuildRequires: freetype-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: zlib-devel

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
Requires: libjpeg-devel
Requires: zlib-devel

%description devel
Development files for python-imaging.


%prep
%autosetup -n %{name}-%{version}/Pillow

%build
%py3_build

%install
mkdir -p %{buildroot}%{py_incdir}/Imaging
install -m 644 src/libImaging/*.h %{buildroot}%{py_incdir}/Imaging
%py3_install


# There is no need to ship the binaries since they are already packaged
# in %doc
rm -rf %{buildroot}%{_bindir}

# Separate files that need Tk and files that don't
echo '%%defattr (0644,root,root,755)' > files.main
p="$PWD"

pushd %{buildroot}%{python3_sitearch}/PIL
for file in *; do
    case "$file" in
    *)
        what=files.main
        ;;
    esac
    echo %{python3_sitearch}/PIL/$file >> "$p/$what"
done
popd

%check
PYTHONPATH=$(ls -1d build/lib.linux*) %{__python3} selftest.py --installed

%files -f files.main
%defattr (-,root,root,-)
%dir %{python3_sitearch}/PIL
%{python3_sitearch}/*.egg-info

%files devel
%defattr (0644,root,root,755)
%{py_incdir}/Imaging
