# K-2SO

> Automation of Let's Encrypt wildcard certificate renewal with OVH and DNS challenge.

# Prerequisite

To use this tool, you MUST have:

* a domain name at [OVHcloud](https://ovhcloud.com)
* a server, VM or VPS w/ Linux & Python 3

# Installation

1. Checkout this repository to your server:
```
git clone git@gitlab.com:dumont.jul/k-2so.git /root/ssl
```
1. Install Python 3 packages:
```
python3 -m pip install -r requirements.txt -U
```
1. Create your wildcard certificate:
```
/root/ssl/renew.sh -d *.<domain>
```
You can add multiple domains (e.g.: `-d <domain1>,*.<domain1>,*.<domain2>`)
1. Add a cronjob to automate the renewal (check everyday at 4 am):
```
0 4 * * *       /root/ssl/renew.sh -d <domain> -E -p <post-action>
```
where <post-action> is the action to reload NGinx, Apache, HAProxy, etc. configuration.
