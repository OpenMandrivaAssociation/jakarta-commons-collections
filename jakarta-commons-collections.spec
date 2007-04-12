%define gcj_support	1	
%define _debug_package	%{nil}
%define base_name	collections
%define short_name	commons-%{base_name}
%define name		jakarta-%{short_name}
%define version		3.2
%define release		%mkrel 1.2
%define	section		free
%define	build_tests	0

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
Summary:	Jakarta Commons Collections Package
License:	Apache License
Group:		Development/Java
#Vendor:		JPackage Project
#Distribution:	JPackage
Source0:	http://www.apache.org/dist/jakarta/commons/collections/source/%{short_name}-%{version}-src-MDVCLEAN.tar.bz2
Patch1:		%{name}-javadoc-nonet.patch
Url:		http://jakarta.apache.org/commons/%{base_name}/
BuildRequires:	ant
%if %{build_tests}
BuildRequires:	ant-junit
%endif
BuildRequires:	jpackage-utils >= 0:1.5
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%else
BuildArch:	noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Provides:	%{short_name}
Obsoletes:	%{short_name}

%description
The introduction of the Collections API by Sun in JDK 1.2 has been a
boon to quick and effective Java programming. Ready access to powerful
data structures has accelerated development by reducing the need for
custom container classes around each core object. Most Java2 APIs are
significantly easier to use because of the Collections API.
However, there are certain holes left unfilled by Sun's
implementations, and the Jakarta-Commons Collections Component strives
to fulfill them. Among the features of this package are:
- special-purpose implementations of Lists and Maps for fast access
- adapter classes from Java1-style containers (arrays, enumerations) to
Java2-style collections.
- methods to test or create typical set-theory properties of collections
such as union, intersection, and closure.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch1 -p1
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=
%if %{build_tests}
export OPT_JAR_LIST="ant-junit"
%else
export OPT_JAR_LIST=
%endif
%ant -Djava.io.tmpdir=. jar \
%if %{build_tests}
  test \
%endif
  javadoc

%install
%{__rm} -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 build/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

# fix end-of-line
%{__perl} -pi -e 's/\r\n/\n/g' *.html *.txt

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc PROPOSAL.html README.txt STATUS.html LICENSE.txt RELEASE-NOTES.html
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}


