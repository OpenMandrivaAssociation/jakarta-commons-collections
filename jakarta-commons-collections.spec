# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1
%define _without_maven 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define base_name       collections
%define short_name      commons-%{base_name}
%define section         free

Name:       jakarta-%{short_name}
Version:    3.2
Release:    %mkrel 1.3
Epoch:      0
Summary:    Provides new interfaces, implementations and utilities for Java Collections
License:    Apache Software License 
Group:      Development/Java
Source0:    http://www.apache.org/dist/jakarta/commons/%{base_name}/source/%{short_name}-%{version}-src-MDVCLEAN.tar.bz2
Source1:    pom-maven2jpp-depcat.xsl
Source2:    pom-maven2jpp-newdepmap.xsl
Source3:    pom-maven2jpp-mapdeps.xsl
Source4:    commons-collections-3.1-jpp-depmap.xml
Source5:    commons-build.tar.gz
# svn export -r '{2007-02-15}' http://svn.apache.org/repos/asf/jakarta/commons/proper/commons-build/trunk/ commons-build
# tar czf commons-build.tar.gz commons-build
Source6:    collections-tomcat5-build.xml

Patch0:         %{name}-javadoc-nonet.patch

Url:            http://jakarta.apache.org/commons/%{base_name}/
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  xml-commons-apis >= 1.3
%if %{with_maven}
BuildRequires:  maven >= 0:1.1
BuildRequires:  maven-plugins-base
BuildRequires:  maven-plugin-test
BuildRequires:  maven-plugin-xdoc
BuildRequires:  maven-plugin-license
BuildRequires:  maven-plugin-changes
BuildRequires:  maven-plugin-jdepend
BuildRequires:  maven-plugin-jdiff
BuildRequires:  maven-plugin-jxr
BuildRequires:  maven-plugin-tasklist
BuildRequires:  maven-plugin-developer-activity
BuildRequires:  maven-plugin-file-activity
BuildRequires:  saxon
BuildRequires:  saxon-scripts
%endif

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:  %{_tmppath}/%{name}-buildroot
Provides:   %{short_name} = %{epoch}:%{version}-%{release}
Obsoletes:  %{short_name} < %{epoch}:%{version}-%{release}

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

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

%package testframework
Summary:        Testframework for %{name}
Group:          Development/Testing
Requires:       %{name} = %{epoch}:%{version}-%{release}

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description testframework
%{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation

%description javadoc
%{summary}.

%package tomcat5
Summary:        Jakarta Commons Collection dependency for Tomcat5
Group:          Development/Libraries/Java

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description tomcat5
A package that is specifically designed to fulfill to a Tomcat5 dependency.

%package testframework-javadoc
Summary:        Javadoc for %{name}-testframework
Group:          Development/Documentation

%description testframework-javadoc
%{summary}.

%if %{with_maven}
%package manual
Summary:        Documents for %{name}
Group:          Development/Documentation

%description manual
%{summary}.
%endif

%prep
cat <<EOT

                If you dont want to build with maven,
                give rpmbuild option '--without maven'

EOT

%setup -q -n %{short_name}-%{version}-src
gzip -dc %{SOURCE5} | tar xf -
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0 -p1
cp %{SOURCE6} .

# Fix file eof
%{__sed} -i 's/\r//' STATUS.html
%{__sed} -i 's/\r//' LICENSE.txt
%{__sed} -i 's/\r//' PROPOSAL.html
%{__sed} -i 's/\r//' RELEASE-NOTES.html
%{__sed} -i 's/\r//' README.txt
%{__sed} -i 's/\r//' NOTICE.txt

%build
%if %{with_maven}
export DEPCAT=$(pwd)/commons-collections-3.1-depcat.new.xml
echo '<?xml version="1.0" standalone="yes"?>' > $DEPCAT
echo '<depset>' >> $DEPCAT
for p in $(find . -name project.xml); do
    pushd $(dirname $p)
    /usr/bin/saxon project.xml %{SOURCE1} >> $DEPCAT
    popd
done
echo >> $DEPCAT
echo '</depset>' >> $DEPCAT
/usr/bin/saxon $DEPCAT %{SOURCE2} > commons-collections-3.1-depmap.new.xml

for p in $(find . -name project.xml); do
    pushd $(dirname $p)
    cp project.xml project.xml.orig
    /usr/bin/saxon -o project.xml project.xml.orig %{SOURCE3} map=%{SOURCE4}
    popd
done

export MAVEN_HOME_LOCAL=$(pwd)/.maven

#        -Dmaven.test.failure.ignore=true \
maven \
        -Dmaven.repo.remote=file:/usr/share/maven/repository \
        -Dmaven.home.local=${MAVEN_HOME_LOCAL} \
        jar:jar javadoc:generate xdoc:transform
%ant tf.javadoc
%else
#FIXME Enabling tests with gcj causes memory leaks!
# See http://gcc.gnu.org/bugzilla/show_bug.cgi?id=28423
%if %{gcj_support}
%ant -Djava.io.tmpdir=. jar javadoc tf.validate tf.jar dist.bin dist.src tf.javadoc
%else
%ant -Djava.io.tmpdir=. test dist tf.javadoc
%endif
%endif

# commons-collections-tomcat5
%ant -f collections-tomcat5-build.xml

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
%if %{with_maven}
install -m 644 target/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 target/%{short_name}-testframework-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-testframework-%{version}.jar
%else
install -m 644 build/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 build/%{short_name}-testframework-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-testframework-%{version}.jar
%endif

#tomcat5
install -m 644 collections-tomcat5/%{short_name}-tomcat5.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tomcat5-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
cp -pr build/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf target/docs/apidocs

# testframework-javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework-%{version}
cp -pr build/docs/testframework/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework-%{version}
ln -s %{name}-testframework-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testframework 

# manual
%if %{with_maven}
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr target/docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%endif

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif

%post testframework
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun testframework
%if %{gcj_support}
%{clean_gcjdb}
%endif

%post tomcat5
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun tomcat5 
%if %{gcj_support}
%{clean_gcjdb}
%endif


%files
%defattr(0644,root,root,0755)
%doc PROPOSAL.html README.txt STATUS.html LICENSE.txt RELEASE-NOTES.html NOTICE.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{short_name}-%{version}.jar
%{_javadir}/%{short_name}.jar

%if %{gcj_support}
# (anssi) own the dir:
%dir  %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/jakarta-commons-collections-%{version}.jar.*
%endif

%files testframework
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-testframework-%{version}.jar
%{_javadir}/%{name}-testframework.jar
%{_javadir}/%{short_name}-testframework-%{version}.jar
%{_javadir}/%{short_name}-testframework.jar

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/jakarta-commons-collections-testframework-%{version}.jar.*
%endif

%files tomcat5
%defattr(0644,root,root,0755)
%{_javadir}/*-tomcat5*.jar
%doc LICENSE.txt NOTICE.txt
%if %{gcj_support}
# (anssi) own the dir:
%dir  %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*-tomcat5*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files testframework-javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-testframework-%{version}
%{_javadocdir}/%{name}-testframework

%if %{with_maven}
%files manual
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}
%endif

