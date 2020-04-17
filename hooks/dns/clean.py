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

# Check if challenge is still existing
if hook.is_challenge_exists():
    hook.remove_challenge()

