# K-2SO

> Automation of Let's Encrypt wildcard certificate renewal with OVH and DNS challenge.

## Prerequisite

To use this tool, you MUST have:

* a domain name at [OVHcloud](https://ovhcloud.com)
* a server, VM or VPS w/ Linux & Python 3
* Certbot >= 1.1

## Installation

1. Download latest revision (MUST be root):
```
wget 'https://gitlab.com/dumont.jul/k-2so/-/archive/master/k-2so-master.tar.gz'
tar -xvvzf k-2so-master.tar.gz
```
2. Install Python 3 packages:
```
mv k-2so-master /root/ssl
cd /root/ssl
python3 -m pip install -r requirements.txt -U
```
3. Create an [API token from OVH](https://eu.api.ovh.com/createToken/), with permissions:
```
POST /domain/zone/*
GET /domain/zone/*
DELETE /domain/zone/*
```
4. Update _config.ini_ with the information
5. Create your wildcard certificate (you can add multiple domains - e.g.: `-d <domain1>,*.<domain1>,*.<domain2>`):
```
/root/ssl/renew.sh -d <domain> -E
```
1. Add a cronjob to automate the renewal (check everyday at 4 am); where <post-action> is the action to reload NGinx, Apache, HAProxy, etc. configuration:
```
0 4 * * *       /root/ssl/renew.sh -d <domain> -E -p <post-action>
```
