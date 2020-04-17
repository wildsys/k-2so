#!/usr/bin/env python3
# coding: utf-8

# Imports
import ovh
import sys
import logging
import os
import dns.resolver


# Class
class K2SODNSHook:

    def __init__(self, **kwargs):
        self.prefix = '_acme-challenge'
        self.logger = logging.getLogger('K2SODNSHook')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('/tmp/marvin-certbot.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        for var in ['CERTBOT_DOMAIN', 'CERTBOT_VALIDATION', 'CERTBOT_TOKEN', 'CERTBOT_AUTH_OUTPUT']:
            attribute_name = var[8:].lower()
            var_value = os.environ.get(var, None)
            self.logger.debug('{} = {}'.format(attribute_name, var_value))
            setattr(self, attribute_name, var_value)
        self.ovh = ovh.Client(
            endpoint=kwargs.get('endpoint'),
            application_key=kwargs.get('application_key'),
            application_secret=kwargs.get('application_secret'),
            consumer_key=kwargs.get('consumer_key')
        )

    def master_domain(self):
        if self.domain.count('.') == 1:
            return self.domain
        sl = self.domain.split('.')
        return '{}.{}'.format(sl[-2], sl[-1])

    def existing_challenges(self):
        sub_domain = '{}.{}'.format(self.prefix, self.domain.replace(self.master_domain(), '').strip('.')).strip('.')
        self.logger.debug('Get challenges records for {}'.format(self.master_domain()))
        challenges = []
        record_ids = self.ovh.get('/domain/zone/{}/record'.format(self.master_domain()))
        for rid in record_ids:
            record = self.ovh.get('/domain/zone/{}/record/{}'.format(self.master_domain(), rid))
            if record['fieldType'] == 'TXT' and record['subDomain'] == sub_domain:
                challenges.append(record['target'].strip('"'))
        return challenges

    def is_challenge_exists(self):
        return self.validation in self.existing_challenges()

    def refresh_soa(self):
        self.logger.info('Refresh {} SOA'.format(self.master_domain()))
        record = self.ovh.post('/domain/zone/{}/refresh'.format(self.master_domain()))

    def write_challenge(self):
        sub_domain = '{}.{}'.format(self.prefix, self.domain.replace(self.master_domain(), '').strip('.')).strip('.')
        self.logger.info('Write challenge on OVH servers: {} ({}:TXT)= {}'.format(sub_domain, self.master_domain(), self.validation))
        self.ovh.post('/domain/zone/{}/record'.format(self.master_domain()),
            fieldType='TXT',
            subDomain=sub_domain,
            target=self.validation,
            ttl=0
        )
        self.refresh_soa()

    def remove_challenge(self):
        sub_domain = '{}.{}'.format(self.prefix, self.domain.replace(self.master_domain(), '').strip('.')).strip('.')
        self.logger.info('Remove challenge on OVH servers: {} ({}:TXT)= {}'.format(sub_domain, self.master_domain(), self.validation))
        record_ids = self.ovh.get('/domain/zone/{}/record'.format(self.master_domain()))
        match_id = None
        for rid in record_ids:
            record = self.ovh.get('/domain/zone/{}/record/{}'.format(self.master_domain(), rid))
            if record['fieldType'] == 'TXT' and record['subDomain'] == sub_domain and record['target'] == self.validation:
                match_id = rid
                break
        if match_id is None:
            self.logger.warning('No challenge to remove. Please use is_challenge_exists() method before using remove_challenge()')
            sys.exit(1)
        self.logger.debug('Remove record ID {}'.format(match_id))
        self.ovh.delete('/domain/zone/{}/record/{}'.format(self.master_domain(), match_id))
        self.refresh_soa()

    def resolve_challenge(self):
        """
        resolve_challenge()
        Request an external DNS server (non-OVH) in order to ensure the challenge is propagated.
        Different from the existing_challenges, which returns list of challenges on OVH servers.
        """
        query_domain = '{}.{}'.format(self.prefix, self.domain)
        results = dns.resolver.query(query_domain, 'TXT', source='8.8.8.8')
        is_challenge_resolved = False
        for result in results:
            if result.target == self.validation:
                is_challenge_resolved = True
        return is_challenge_resolved


# Not an executable script
if __name__ == '__main__':
    sys.exit(1)

