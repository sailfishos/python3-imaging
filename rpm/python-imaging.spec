%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define pyver %(%{__python} -c "import sys ; print sys.version[:3]")
%define py_incdir %{_includedir}/python%{pyver}

Summary:       Python's own image processing library
Name:          python-imaging
Version:       2.2.0
Release:       14

License:       BSD
Group:         System/Libraries

Source0:       %{name}-%{version}.tar.gz
URL:           http://www.pythonware.com/products/pil/

BuildRequires: python-devel, libjpeg-devel, zlib-devel, freetype-devel, python-setuptools, lcms-devel, libtiff-devel

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
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, python-devel
Requires: libjpeg-devel
Requires: zlib-devel

%description devel
Development files for python-imaging.


%prep
%setup -q -n %{name}-%{version}/Pillow

%build
# Is this still relevant? (It was used in 1.1.4)
#%ifarch x86_64
#   CFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC" \
#%endif

CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{py_incdir}/Imaging
install -m 644 libImaging/*.h $RPM_BUILD_ROOT/%{py_incdir}/Imaging
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


# There is no need to ship the binaries since they are already packaged
# in %doc
rm -rf $RPM_BUILD_ROOT%{_bindir}

# Separate files that need Tk and files that don't
echo '%%defattr (0644,root,root,755)' > files.main
p="$PWD"

pushd $RPM_BUILD_ROOT%{python_sitearch}/PIL
for file in *; do
    case "$file" in
    *)
        what=files.main
        ;;
    esac
    echo %{python_sitearch}/PIL/$file >> "$p/$what"
done
popd


%check
PYTHONPATH=$(ls -1d build/lib.linux*) %{__python} selftest.py

%clean
rm -rf $RPM_BUILD_ROOT


%files -f files.main
%defattr (-,root,root,-)
%dir %{python_sitearch}/PIL
/usr/lib/python2.7/site-packages/Pillow-2.1.0-py2.7.egg-info

%files devel
%defattr (0644,root,root,755)
%{py_incdir}/Imaging
