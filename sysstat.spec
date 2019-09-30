Name:    sysstat
Version: 12.1.6
Release: 1
Summary: System performance tools for the Linux operating system
License: GPLv2+
URL:     http://sebastien.godard.pagesperso-orange.fr/
Source0: http://sebastien.godard.pagesperso-orange.fr/%{name}-%{version}.tar.xz
Source1: colorsysstat.csh
Source2: colorsysstat.sh

BuildRequires: gcc, gettext, lm_sensors-devel, systemd

Requires: findutils, xz
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Patch9000: bugfix-sysstat-10.1.5-read-ttyAMA-first-for-arm64.patch


%description
The sysstat package contains various utilities, common to many commercial 
Unixes, to monitor system performance and usage activity:
iostat: reports CPU statistics and input/output statistics for block devices 
and partitions.
mpstat: reports individual or combined processor related statistics.
pidstat: reports statistics for Linux tasks (processes) : I/O, CPU, memory, etc.
tapestat: reports statistics for tape drives connected to the system.
cifsiostat: reports CIFS statistics.
Sysstat also contains tools you can schedule via cron or systemd to collect and 
historize performance and activity data:
sar： collects, reports and saves system activity information (see below a list 
of metrics collected by sar).
sadc： is the system activity data collector, used as a backend for sar.
sa1： collects and stores binary data in the system activity daily data file.
 It is a front end to sadc designed to be run from cron or systemd.
sa2： writes a summarized daily activity report. It is a front end to sar 
designed to be run from cron or systemd.
sadf： displays data collected by sar in multiple formats (CSV, XML, JSON, etc.)
 and can be used for data exchange with other programs. This command can also 
be used to draw graphs for the various activities collected by sar using SVG (
Scalable Vector Graphics) format.

%prep
%autosetup -n %{name}-%{version} -p1

%build
export sadc_options="-S DISK"
export history="28"
export compressafter="31"
%configure \
    --docdir=%{_pkgdocdir} \
    --enable-install-cron \
    --enable-copy-only \
    --disable-file-attr \
    --disable-stripping
%make_build

%install
%make_install
%find_lang %{name}
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

%check

%pre

%preun
%systemd_preun sysstat.service sysstat-collect.timer sysstat-summary.timer
[ "$1" -gt 0 ] || rm -rf %{_localstatedir}/log/sa/*

%post
%systemd_post sysstat.service sysstat-collect.timer sysstat-summary.timer

%postun
%systemd_postun sysstat.service sysstat-collect.timer sysstat-summary.timer

%files -f %{name}.lang
%doc CHANGES COPYING CREDITS FAQ.md README.md %{name}-%{version}.lsm
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat.ioconf
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_libdir}/sa
%{_unitdir}/sysstat*
%{_localstatedir}/log/sa
%{_mandir}/man*/*

%changelog
* Sat Sep 07 2019 openEuler Buildteam <buildteam@openeuler.org> - 12.1.6-1
- Package init

