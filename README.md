# bind9-ddns-updater-django
# DDNS UPDATER
You can update a 'A' record with on bind9 zone config file with ddns_client.py
This Release works with Python3.8

# Configuration of the system  
## 1-)Create a Linux User (python will work under this user)

Befeore the running this program please backup your bind9 record configuration file !
```sh
$ adduser django
```
## 2-)Disable remote login 'django' user
```sh
$ usermod -L django
```
## 3-)Get the Code
```sh
$ sudo su django
$ cd ~
$ wget https://github.com/egemeric/bind9-ddns-updater-django/archive/v1.0.zip
$ unzip v1.0.zip
$ cd bind9-ddns-updater-django-1.0
```
## 4-) Create Virtual Env and activate environment

```sh
$ python3.8 -m venv env
$ source env/bin/activate
```
## 5-) Test the virt env

```sh
$ which python
```
if you see the your directory location your virt env, it is ok.

## 6-)Add user Django to sudoers

append end line of the file /etc/sudoers/  
if you use debian 9 or 10 you should install sudo via apt.
```sh
$ django ALL=(ALL) NOPASSWD: /etc/init.d/bind9 reload
```
by adding this, django user will run the reload command with python under root permissions.  
if your distribution is different edit  the' /etc/init.d/bind9 reload' section.

## 7-) Edit settings.py

if your bind9 zone file like this file format(Updater/dns.conf) this program will work. if your configuration file is different ,you must edit regex_query by own.
Enter your config bind9 config location
```python
BIND9_FILE = '/etc/bind/master/example.com'
```
And add your root domain, at this release you can not edit root record you can only update subdomains
```python
ROOT_DOMAIN = 'example.com'
```
Also you have to add your subdomain record under the bind9 config file like this
```sh
updatedsubdomainname			60	A	192.168.1.1

Also you can disable DEBUG mode under settings.py
```python
DEBUG = False
```
## 8-) To create sqlite file migrate app with manage.py and Run the server
```sh
python manage.py migrate
```
After that create superuser to mange domains 
```sh
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```
## 9-) Client
->you can use my client under Client directory with name ddns_client.py. 
->you will see the variables under of the script and edit them by own. 
->you can use client via crontab to make update request  


