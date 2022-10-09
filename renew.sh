#!/bin/bash

# Required arguments
DOMAINS=''
POST_ACTIONS=''
CONTACT_MAIL=''
DRY_RUN='--dry-run'
ALT_HOOKS="$(dirname $0)/hooks/dns"
while getopts "k:d:p:e:E" opt
do
    case $opt
    in
        'd') DOMAINS=$OPTARG ;;
        'E') DRY_RUN='' ;;
        'p') POST_ACTIONS=$OPTARG ;;
        'e') CONTACT_MAIL=$OPTARG ;;
        'k') ALT_HOOKS=$OPTARG ;;
        ?) exit 1 ;;
    esac
done
test -z $DOMAINS && echo -e "Usage: $0 -d <domain(s)> -e <contact_email> [-E] [-p <post_actions>] [-k <hook_directory>]" && exit 1
test -z $CONTACT_MAIL && echo -e "Usage: $0 -d <domain(s)> -e <contact_email> [-E] [-p <post_actions>] [-k <hook_directory>]" && exit 1

# Certbot execution
certbot \
    -n \
    -d $DOMAINS \
    --manual \
    --expand \
    $DRY_RUN \
    --agree-tos \
    --email $CONTACT_MAIL \
    --manual-public-ip-logging-ok \
    --preferred-challenges dns \
    --manual-auth-hook ${ALT_HOOKS}/auth.py \
    --manual-cleanup-hook ${ALT_HOOKS}/clean.py \
    certonly
$($POST_ACTIONS)
