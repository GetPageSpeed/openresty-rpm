%define _debugsource_template %{nil}
%global version_cli 0.27
# OpenResty is compatible with 5.1 only! We must build 5.1 version always, even on <= EL8
%global luacompatver %{nil}
%if 0%{?fedora} || 0%{?rhel} > 7
%global luacompatver 5.1
%endif

Name:           openresty
Version:        1.21.4.1
Release:        7%{?dist}
Summary:        OpenResty, fast web app server extending NGINX

License:        BSD
URL:            http://openresty.org/
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1:        https://github.com/%{name}/resty-cli/archive/v%{version_cli}/resty-cli-v%{version_cli}.tar.gz
Group:          System Environment/Daemons
Requires:       nginx-module-lua 
Requires:       nginx-module-stream-lua
Requires:       nginx-module-coolkit
Requires:       nginx-module-encrypted-session
Requires:       nginx-module-form-input
Requires:       nginx-module-xss

Requires:       lua%{luacompatver}-rds-parser
Requires:       lua%{luacompatver}-resty-shell
Requires:       lua%{luacompatver}-resty-signal
Requires:       lua%{luacompatver}-resty-dns

BuildArch:      noarch

%description
This package is a metapackage allowing you to set up an OpenResty NGINX
instance. Built for production uses.

It pulls in all the packages associated with OpenResty, and auto-enables
related modules.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

By taking advantage of various well-designed Nginx modules (most of which
are developed by the OpenResty team themselves), OpenResty effectively
turns the nginx server into a powerful web app server, in which the web
developers can use the Lua programming language to script various existing
nginx C modules and Lua modules and construct extremely high-performance
web applications that are capable to handle 10K ~ 1000K+ connections in
a single box.


%package resty

Summary:        OpenResty command-line utility, resty
Group:          Development/Tools
Requires:       perl, openresty >= %{version}-%{release}
Requires:       perl(File::Spec), perl(FindBin), perl(List::Util), perl(Getopt::Long), perl(File::Temp), perl(POSIX), perl(Time::HiRes)
BuildArch:      noarch


%description resty
This package contains the "resty" command-line utility for OpenResty, which
runs OpenResty Lua scripts on the terminal using a headless NGINX behind the
scene.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

%prep
%autosetup
tar xzf %{SOURCE1}
# patch up resty cli so that it uses /sbin/nginx by default instead of searching
sed -i 's@my $nginx_path;@my $nginx_path = "/sbin/nginx";@' \
  resty-cli-%{version_cli}/bin/resty
# ensure generated .conf file has dynamic Lua module enabled
# ensure absolute paths to module files as relative will not work
sed -i "s@^\daemon off;@daemon off;\nload_module %{_libdir}/nginx/modules/ngx_stream_lua_module.so;\n@" \
 resty-cli-%{version_cli}/bin/resty
sed -i "s@^\daemon off;@daemon off;\nload_module %{_libdir}/nginx/modules/ngx_http_lua_module.so;\n@" \
 resty-cli-%{version_cli}/bin/resty
sed -i "s@^\daemon off;@daemon off;\nload_module %{_libdir}/nginx/modules/ndk_http_module.so;\n@" \
 resty-cli-%{version_cli}/bin/resty


%build
# nothing to do, yet?


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
%{__install} -Dpm0755 resty-cli-%{version_cli}/bin/resty %{buildroot}%{_bindir}/resty


%files
%license COPYRIGHT
%doc README.markdown


%files resty
%{_bindir}/resty


%changelog
* Thu Apr  1 2021 Danila Vershinin <info@getpagespeed.com>
- initial packaging
