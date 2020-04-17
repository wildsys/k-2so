#!/bin/bash

# Required arguments
DOMAINS=''
POST_ACTIONS=''
DRY_RUN='--dry-run'
while getopts "d:p:E" opt
do
    case $opt
    in
        'd') DOMAINS=$OPTARG ;;
        'E') DRY_RUN='' ;;
        'p') POST_ACTIONS=$OPTARG ;;
        ?) exit 1 ;;
    esac
done
test -z $DOMAINS && echo -e "Usage: $0 -d <domain(s)> [-E] [-p <post_actions>]" && exit 1

# Certbot execution
certbot \
    -n \
    -d $DOMAINS \
    --manual \
    --expand \
    $DRY_RUN \
    --manual-public-ip-logging-ok \
    --preferred-challenges dns \
    --manual-auth-hook $(dirname $0)/hooks/dns/auth.py \
    --manual-cleanup-hook $(dirname $0)/hooks/dns/clean.py \
    certonly
$POST_ACTIONS

