%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           supybot-notify
Version:        0.1
Release:        1%{?dist}
Summary:        Notification plugin for Supybot

Group:          Applications/Internet
License:        BSD
URL:            http://fedorapeople.org/gitweb?p=ricky/public_git/supybot-notify.git;a=summary
Source0:        http://ricky.fedorapeople.org/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       supybot

BuildArch:      noarch
BuildRequires:  python-devel

%description
A Supybot plugin which relays messages from a TCP server to
an IRC channel.


%prep
%setup -q


%build


%install
%{__rm} -rf %{buildroot}
%{__install} -dm 755 %{buildroot}/%{python_sitelib}/supybot/plugins/Notify
%{__install} -pm 644 *.py %{buildroot}/%{python_sitelib}/supybot/plugins/Notify


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.txt
%{python_sitelib}/supybot/plugins/Notify


%changelog
* Mon Mar 16 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.1-1
- Initial RPM package.
