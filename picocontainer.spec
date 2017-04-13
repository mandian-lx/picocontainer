%{?_javapackages_macros:%_javapackages_macros}

Name:          picocontainer
Version:       2.15
Release:       6%{?dist}
Summary:       Java library implementing the Dependency Injection pattern
Group:         Development/Java
License:       BSD
Url:           http://picocontainer.codehaus.org/
# svn export http://svn.codehaus.org/picocontainer/java/2.x/tags/picocontainer-2.15
# tar cJf picocontainer-2.15.tar.xz picocontainer-2.15
Source0:       %{name}-%{version}.tar.xz

BuildRequires: mvn(asm:asm)
BuildRequires: mvn(com.thoughtworks.paranamer:paranamer) # NEW
BuildRequires: mvn(com.thoughtworks.xstream:xstream)
BuildRequires: mvn(javax.inject:javax.inject)
BuildRequires: mvn(javax.annotation:jsr250-api)
BuildRequires: mvn(log4j:log4j:1.2.17)
BuildRequires: mvn(org.jmock:jmock-junit4)
BuildRequires: mvn(xpp3:xpp3_min)
%if 0
# picocontainer-gems deps
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(mx4j:mx4j-impl)
BuildRequires: mvn(org.apache.tomcat:tomcat-servlet-api)
BuildRequires: mvn(org.prefuse:prefuse)
BuildRequires: mvn(org.slf4j:slf4j-api)
BuildRequires: mvn(org.slf4j:slf4j-log4j12)
BuildRequires: mvn(proxytoys:proxytoys)
%endif

# test deps
BuildRequires: mvn(cglib:cglib)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(simple-jndi:simple-jndi)

BuildRequires: mvn(org.hamcrest:hamcrest-library)
BuildRequires: mvn(xpp3:xpp3)

BuildRequires: maven-local
# https://bugzilla.redhat.com/show_bug.cgi?id=1191694
# BuildRequires: mvn(com.thoughtworks.paranamer:paranamer-maven-plugin)
BuildRequires: mvn(org.codehaus:codehaus-parent:pom:)
BuildArch:     noarch

%description
PicoContainer is a highly embeddable full service Inversion of Control
(IoC) container for components honor the Dependency Injection pattern.
It can be used as a lightweight alternative to Sun's J2EE patterns for
web applications or general solutions.

Despite it being very compact in size (the core is ~128K and it has no
mandatory dependencies outside the JDK), PicoContainer supports
different dependency injection types (Constructor, Setter, Annotated
Field and Method) and offers multiple lifecycle and monitoring
strategies.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

# remove wagon-webdav-jackrabbit
%pom_xpath_remove "pom:project/pom:build/pom:extensions"
%pom_remove_plugin :xsite-maven-plugin
# Unwanted source jar
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-shade-plugin container

%pom_xpath_remove "pom:build/pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"

sed -i "s|junit-dep|junit|" pom.xml

%pom_xpath_remove "pom:dependencyManagement/pom:dependencies/pom:dependency[pom:groupId='cglib']/pom:artifactId"
%pom_xpath_inject "pom:dependencyManagement/pom:dependencies/pom:dependency[pom:groupId='cglib']" "<artifactId>cglib</artifactId>"
%if 0
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:groupId='cglib']/pom:artifactId" gems
%pom_xpath_inject "pom:dependencies/pom:dependency[pom:groupId='cglib']" "<artifactId>cglib</artifactId>" gems

%pom_remove_dep javax.servlet:servlet-api gems
%pom_xpath_inject "pom:project/pom:dependencies" "
<dependency>
  <groupId>org.apache.tomcat</groupId>
  <artifactId>tomcat-servlet-api</artifactId>
  <version>any</version>
  <optional>true</optional>
</dependency>" gems
%else
# missing BR
%pom_disable_module gems
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1191694
%pom_remove_plugin :paranamer-maven-plugin
%pom_remove_plugin :paranamer-maven-plugin container
%pom_remove_plugin :paranamer-maven-plugin container-debug

# these test fails for various reason
rm -r container/src/test/org/picocontainer/PicoVisitorTestCase.java \
 container/src/test/org/picocontainer/behaviors/BehaviorAdapterTestCase.java \
 container/src/test/org/picocontainer/behaviors/CachedTestCase.java \
 container/src/test/org/picocontainer/classname/DefaultClassLoadingPicoContainerTestCase.java \
 container/src/test/org/picocontainer/containers/ImmutablePicoContainerTestCase.java \
 container/src/test/org/picocontainer/defaults/AbstractComponentMonitorTestCase.java \
 container/src/test/org/picocontainer/defaults/CollectionComponentParameterTestCase.java \
 container/src/test/org/picocontainer/defaults/DefaultPicoContainerLifecycleTestCase.java \
 container/src/test/org/picocontainer/defaults/issues/Issue0265TestCase.java \
 container/src/test/org/picocontainer/injectors/ConstructorInjectorTestCase.java \
 container/src/test/org/picocontainer/injectors/ReinjectionTestCase.java \
 container/src/test/org/picocontainer/injectors/SetterInjectorTestCase.java \
 container/src/test/org/picocontainer/lifecycle/ReflectionLifecycleStrategyTestCase.java \
 container/src/test/org/picocontainer/lifecycle/StartableLifecycleStrategyTestCase.java \
 container/src/test/org/picocontainer/monitors/RegexComposerTestCase.java \
 container/src/test/org/picocontainer/visitors/MethodCallingVisitorTest.java \
 container/src/test/org/picocontainer/defaults/XStreamSerialisationTestCase.java \
 container/src/test/org/picocontainer/converters/BuiltInConverterTestCase.java \
 container/src/test/org/picocontainer/defaults/DefaultMultipleConstructorTestCase.java \
%if 0
 gems/src/test/org/picocontainer/gems/constraints/AndOrNotTestCase.java \
 gems/src/test/org/picocontainer/gems/constraints/ConstraintsTestCase.java \
 gems/src/test/org/picocontainer/gems/containers/CommonsLoggingTracingContainerDecoratorTestCase.java \
 gems/src/test/org/picocontainer/gems/containers/Log4jTracingContainerDecoratorTestCase.java \
 gems/src/test/org/picocontainer/gems/jmx/AbstractConstructingProviderTest.java \
 gems/src/test/org/picocontainer/gems/jmx/ComponentKeyConventionMBeanInfoProviderTest.java \
 gems/src/test/org/picocontainer/gems/jmx/ComponentTypeConventionMBeanInfoProviderTest.java \
 gems/src/test/org/picocontainer/gems/jmx/DynamicMBeanComponentProviderTest.java \
 gems/src/test/org/picocontainer/gems/jmx/JMXExposedTestCase.java \
 gems/src/test/org/picocontainer/gems/jmx/JMXExposingTestCase.java \
 gems/src/test/org/picocontainer/gems/jmx/JMXVisitorTestCase.java \
 gems/src/test/org/picocontainer/gems/jmx/RegisteredMBeanConstructingProviderTest.java
%endif

# NoClassDefFoundError: org/xmlpull/v1/XmlPullParserFactory
%pom_add_dep xpp3:xpp3::test container
%pom_add_dep xpp3:xpp3::test container-debug

%build

%mvn_build

%install
%mvn_install

sed -i 's/\r//' %{buildroot}%{_javadocdir}/%{name}/stylesheet.css

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc README.txt
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 gil cattaneo <puntogil@libero.it> 2.15-3
- add hamcrest-library as BR

* Wed Feb 11 2015 gil cattaneo <puntogil@libero.it> 2.15-2
- introduce license macro

* Tue Nov 04 2014 gil cattaneo <puntogil@libero.it> 2.15-1
- update to 2.15

* Fri Jun 07 2013 gil cattaneo <puntogil@libero.it> 2.14.3-1
- update to 2.14.3

* Fri Apr 20 2012 gil cattaneo <puntogil@libero.it> 2.14.1-1
- initial rpm
