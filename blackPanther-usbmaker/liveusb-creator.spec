%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define 	oname    liveusb-creator

Name:           blackPanther-liveusb-creator
Version:        3.9.2
Release:        %mkrel 2
Summary:        A liveusb creator

Group:          Applications/System
License:        GPLv2
URL:            http://www.blackpantheros.eu
Source0:        %{oname}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{oname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
ExcludeArch:    ppc
ExcludeArch:    ppc64

BuildRequires:  python-devel, python-setuptools, python-qt4-devel, desktop-file-utils gettext
Requires:       syslinux, python-qt4, usermode, mtools, coreutils
Requires:       python-urlgrabber
Requires:       pyparted >= 2.0

%description
A liveusb creator from blackPanther OS images

%prep
%setup -q -n %oname-%version

%build
%{__python} setup.py build
#make pot
make mo

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf liveusb/urlgrabber

# Adjust for console-helper magic
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/%{oname} %{buildroot}%{_sbindir}/%{oname}
ln -s ../bin/consolehelper %{buildroot}%{_bindir}/%{oname}
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m0640 %{oname}.pam %{buildroot}%{_sysconfdir}/pam.d/%{oname}
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
install -m0640 %{oname}.console %{buildroot}%{_sysconfdir}/security/console.apps/%{oname}

install -m644 boot.7z -D %{buildroot}%{_datadir}/liveusb/boot.7z

desktop-file-install --vendor="blackPanther" \
--dir=%{buildroot}%{_datadir}/applications \
%{buildroot}/%{_datadir}/applications/liveusb-creator.desktop
rm -rf %{buildroot}/%{_datadir}/applications/liveusb-creator.desktop
%find_lang %{oname}


# Generate binary
cd %{buildroot}
python -m compileall .
find %{buildroot}%_libdir -name "*.py" | xargs rm -f


%clean
rm -rf %{buildroot}

#*********************************************************************************************************
#*   __     __               __     ______                __   __                      _______ _______   *
#*  |  |--.|  |.---.-..----.|  |--.|   __ \.---.-..-----.|  |_|  |--..-----..----.    |       |     __|  *
#*  |  _  ||  ||  _  ||  __||    < |    __/|  _  ||     ||   _|     ||  -__||   _|    |   -   |__     |  *
#*  |_____||__||___._||____||__|__||___|   |___._||__|__||____|__|__||_____||__|      |_______|_______|  *
#* http://www.blackpantheros.eu | http://www.blackpanther.hu - kbarcza[]blackpanther.hu * Charles Barcza *
#*************************************************************************************(c)2002-2011********

%define bin %_bindir
%define app  -n %name
%define appl %name
%pre %app
if [ ! -f /etc/blackPanther-release ];then
    xmsg=`which kdialog 2>/dev/null|| which zenity 2>/dev/null|| echo`
           [ -n "$DISPLAY" ] && $xmsg --error "This is the system not a blackPanther OS, please download and try it: www.blackpanther.hu"
           [ ! -n "$DISPLAY" ] && echo -n "This is the system not a blackPanther OS, please download and try it: www.blackpanther.hu"
fi

######## This function Copyright(c) use Only blackPanrher OS packages
if [ -f /etc/blackPanther-release ] && [ -f %bin/%appl ]; then
    touch /tmp/.rpm%{name}
fi

%post %app
######## This function Copyright(c) use Only blackPanrher OS packages
if [ -f /etc/blackPanther-release ] && [ -n "$DISPLAY"  ];then
 if [ -f /tmp/.rpm%{name} ]; then
    bubblemsg upgrade %{appl}
    rm -f /tmp/.rpm%{name}
      else
     bubblemsg install %{appl}
    fi

fi

%postun %app
######## This function Copyright(c) Only blackPanrher OS packages
if [ -f /etc/blackPanther-release ] && [ -n "$DISPLAY" ];then
    if [ ! -f %bin/%appl ]; then
	bubblemsg uninstall %{appl}
    fi
fi


%files -f %{oname}.lang
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python_sitelib}/*
%{_bindir}/%{oname}
%{_sbindir}/%{oname}
%{_datadir}/applications/*.desktop
%{_datadir}/liveusb/boot.7z
%{_datadir}/pixmaps/blackpantherusb.png
%config(noreplace) %{_sysconfdir}/pam.d/%{oname}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{oname}

%changelog
* Mon Feb 21 2011 Charles Barcza <info@blackpanther.hu> 
- import for blackPanther OS v11.x
---------------------------------------------------------
