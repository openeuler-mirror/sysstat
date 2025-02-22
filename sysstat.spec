Name:    sysstat
Version: 12.6.2
Release: 2
Summary: System performance tools for the Linux operating system
License: GPLv2+
URL:     http://sebastien.godard.pagesperso-orange.fr/
Source0: https://github.com/sysstat/sysstat/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

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

%check
./do_test

%pre

%preun
%systemd_preun sysstat.service sysstat-collect.timer sysstat-summary.timer
[ "$1" -gt 0 ] || rm -rf %{_localstatedir}/log/sa/*

%post
%systemd_post sysstat.service sysstat-collect.timer sysstat-summary.timer

%postun
%systemd_postun sysstat.service sysstat-collect.timer sysstat-summary.timer

%posttrans
/usr/bin/systemctl enable sysstat.service >/dev/null 2>&1

%files -f %{name}.lang
%doc CHANGES COPYING CREDITS FAQ.md README.md %{name}-%{version}.lsm
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat.ioconf
%{_bindir}/*
%{_libdir}/sa
%{_unitdir}/../*
%{_localstatedir}/log/sa
%{_mandir}/man*/*

%changelog
* Fri Apr 14 2023 wangjiang <wangjiang37@h-partners.com> - 12.6.2-2
- service auto start after install

* Fri Feb 03 2023 zhangpan <zhangpan@h-partners.com> - 12.6.2-1
- update to 12.6.2

* Fri Nov 25 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 12.5.4-5
- update Source0

* Thu Nov 10 2022  zhouwenpei <zhouwenpei1@h-partners.com> - 12.5.4-4
- fix CVE-2022-39377

* Mon Jun 13 2022  wuchaochao <cyanrose@yeah.net> - 12.5.4-3
- add check

* Sat May 7 2022 dongyuzhen <dongyuzhen@h-partners.com> - 12.5.4-2
- add missing changelog

* Sat Dec 4 2021 wuchaochao <wuchaochao4@h-partners.com> - 12.5.4-1
- update version to 12.5.4

* Tue Feb 2 2021 yuanxin <yuanxin24@huawei.com> - 12.5.2-1
- Upgrade version to 12.5.2

* Thu Jun 11 2020 hanhui<hanhui15@huawei.com> - 12.2.2
- update version to 12.2.2

* Fri May 29 2020 openEuler Buildteam <buildteam@openeuler.org> - 12.1.6-3
- rebuild for lm_sensors version update

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 12.1.6-2
- Delete useless files.

* Sat Sep 07 2019 openEuler Buildteam <buildteam@openeuler.org> - 12.1.6-1
- Package init

