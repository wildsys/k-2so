#!/usr/bin/env python3
# coding: utf-8

# Imports
from libdns import K2SODNSHook
import time
import sys
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Instance
hook = K2SODNSHook(
    application_key=config.get('OVH', 'key'),
    application_secret=config.get('OVH', 'secret'),
    endpoint=config.get('OVH', 'endpoint'),
    consumer_key=config.get('OVH', 'consumer')
)

# If challenge does not exists on OVH DNS servers, we create it
if not hook.is_challenge_exists():
    hook.write_challenge()

# Wait for an external validation
time.sleep(2)
retry = 0
is_challenge_success = hook.resolve_challenge()
while not is_challenge_success and retry < 10:
    time.sleep(2)
    retry += 1
    is_challenge_success = hook.resolve_challenge()

# Exit code
sys.exit(0 if is_challenge_success else 1)

