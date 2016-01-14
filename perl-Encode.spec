%{?scl:%scl_package perl-Encode}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}perl-Encode
Epoch:          1
Version:        2.57
Release:        1%{?dist}
Summary:        Character encodings in Perl
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Encode/
Source0:        http://www.cpan.org/authors/id/D/DA/DANKOGAI/Encode-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(File::Spec::Functions)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(warnings)
# Run-time:
BuildRequires:  %{?scl_prefix}perl(bytes)
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(constant)
BuildRequires:  %{?scl_prefix}perl(Exporter) >= 5.57
# Filter::Util::Call is optional
BuildRequires:  %{?scl_prefix}perl(Getopt::Long)
# I18N::Langinfo is optional
BuildRequires:  %{?scl_prefix}perl(MIME::Base64)
BuildRequires:  %{?scl_prefix}perl(overload)
BuildRequires:  %{?scl_prefix}perl(parent) >= 0.221
# PerlIO::encoding is optional
BuildRequires:  %{?scl_prefix}perl(re)
# Storable is optional
BuildRequires:  %{?scl_prefix}perl(utf8)
BuildRequires:  %{?scl_prefix}perl(vars)
BuildRequires:  %{?scl_prefix}perl(XSLoader)
# Tests:
# Benchmark not used
BuildRequires:  %{?scl_prefix}perl(charnames)
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(File::Basename)
BuildRequires:  %{?scl_prefix}perl(File::Compare)
BuildRequires:  %{?scl_prefix}perl(File::Copy)
BuildRequires:  %{?scl_prefix}perl(FileHandle)
BuildRequires:  %{?scl_prefix}perl(FindBin)
BuildRequires:  %{?scl_prefix}perl(IO::Select)
BuildRequires:  %{?scl_prefix}perl(IPC::Open3)
# IPC::Run not used
BuildRequires:  %{?scl_prefix}perl(lib)
BuildRequires:  %{?scl_prefix}perl(Scalar::Util)
BuildRequires:  %{?scl_prefix}perl(Symbol)
BuildRequires:  %{?scl_prefix}perl(Test)
BuildRequires:  %{?scl_prefix}perl(Test::More)
BuildRequires:  %{?scl_prefix}perl(Tie::Scalar)
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Requires:       %{?scl_prefix}perl(parent) >= 0.221

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\((Encode::ConfigLocal|MY)\\)

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{?scl_prefix}perl\\((Exporter|parent)\\)$

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_from_provides /perl(\(Encode::ConfigLocal\|MY\))/d
%filter_from_requires /perl(\(Exporter\|parent\))$/d
%filter_setup
%endif

%description
The Encode module provides the interface between Perl strings and the rest
of the system. Perl strings are sequences of characters.

# To mirror files from perl-devel (bug #456534)
# Keep architecture specific because files go into vendorarch
%package devel
Summary:        Perl Encode Module Generator
Group:          Development/Libraries
Requires:       %{?scl_prefix}%{pkg_name}%{?_isa} = %{epoch}:%{version}-%{release}
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Requires:       %{?scl_prefix}perl-devel
Requires:       %{?scl_prefix}perl(Encode)

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_requires_in  %{perl_vendorarch}/.*Makefile_PL.e2x$
%filter_setup
%endif

%description devel
enc2xs builds a Perl extension for use by Encode from either Unicode Character
Mapping files (.ucm) or Tcl Encoding Files (.enc). You can use enc2xs to add
your own encoding to perl. No knowledge of XS is necessary.


%prep
%setup -q -n Encode-%{version}

%build
# Additional scripts can be installed by appending MORE_SCRIPTS, UCM files by
# INSTALL_UCM.
%{?scl:scl enable %{scl} '}
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
%{?scl:'}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{?scl:"}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}

%files
%doc AUTHORS Changes README
%{_bindir}/piconv
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Encode*
%exclude %{perl_vendorarch}/Encode/*.e2x
%exclude %{perl_vendorarch}/Encode/encode.h
%{perl_vendorarch}/encoding.pm
%{_mandir}/man1/piconv.*
%{_mandir}/man3/*

%files devel
%{_bindir}/enc2xs
%{_mandir}/man1/enc2xs.*
%{perl_vendorarch}/Encode/*.e2x
%{perl_vendorarch}/Encode/encode.h

%changelog
* Wed Jan 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.57-1
- 2.57 bump
- Update filters
- Resolves: rhbz#1049896

* Wed Nov 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.55-2
- Add epoch to devel BR

* Tue Nov 19 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.55-1
- 2.55 bump

* Mon May 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.51-1
- 2.51 bump

* Wed Apr 03 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.49-1
- SCL package - initial import
