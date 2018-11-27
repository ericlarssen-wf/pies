#!/usr/bin/env python

import argparse
from subprocess import call


ENV_MAP = {
    'wk-dev': {
        'admiral_url': 'https://admiral.wk-dev.workiva.org/',
        'admiral_token': '6b343eabf9f28813128bef915f685b09',
        'domain': 'wk-dev.wdesk.org',
    },
    'staging': {
        'admiral_url': 'https://admiral.staging.wdesk.org/',
        'admiral_token': '',
        'domain': 'staging.wdesk.org',
    },
    'inf-tools': {
        'admiral_url': 'https://admiral.inf.workiva.net',
        'admiral_token': '',
        'domain': 'inf.workiva.net',
    },
    'sandbox': {
        'admiral_url': 'https://admiral-sandbox-aws.workiva.net/',
        'admiral_token': '',
        'domain': 'sandbox.wdesk.com',
    },
    'pentest': {
        'admiral_url': 'https://admiral-pentest.workiva.net/',
        'admiral_token': '',
        'domain': 'olympus.wdesk.com',
    },
    'demo': {
        'admiral_url': 'https://admiral-demo.workiva.net/',
        'admiral_token': '',
        'domain': 'demo.wdesk.com',
    },
    'prod': {
        'admiral_url': 'https://admiral-prod-east.workiva.net/',
        'admiral_token': '',
        'domain': 'app.wdesk.com',
    },
    'prod-eu': {
        'admiral_url': 'https://admiral-prod-eu.workiva.net/',
        'admiral_token': '',
        'domain': 'eu.wdesk.com',
    },
}

GITHUB_TOKEN = ''

def get_arg_parser():
    parser = argparse.ArgumentParser(
        description='Migrate service variables from Harbour to Kubernetes'
    )

    parser.add_argument(
        '-s',
        '--service',
        help='Name of Service to migrate.',
        required=True,
    )

    parser.add_argument(
        '-c',
        '--cluster',
        help='Name of cluster the service is migrating.',
        required=True,
    )

    parser.add_argument(
        '-r',
        '--repo',
        help='The repo associated with the service. (ex. cerberus)',
        required=True,
    )

    parser.add_argument(
        '-k',
        '--kms_region',
        help='The region the kms key is stored in. (Dev = us-west-2, Prod = us-east-1)',
        default='us-east-1',
    )

    return parser


def main():
    """
    Command-line entrypoint.
    """
    parser = get_arg_parser()

    args = parser.parse_args()

    service = args.service
    repo = args.repo
    cluster = args.cluster
    region = args.kms_region
    cluster_config = ENV_MAP.get(cluster)

    if not cluster_config:
        print('Cluster config not found, edit this script to set it.')
        exit(1)

    if not GITHUB_TOKEN:
        print('Github token not found, edit this script to set it.')
        exit(1)

    admiral_url = cluster_config.get('admiral_url')
    if not admiral_url:
        print(f'Admiral url not set for {cluster}, edit this script to set it.')
        exit(1)

    admiral_token = cluster_config.get('admiral_token')
    if not admiral_token:
        print(f'Admiral token not set for {cluster}, edit this script to set it.')
        exit(1)

    domain = cluster_config.get('domain')
    if not domain:
        print(f'Domain not set for {cluster}, edit this script to set it.')
        exit(1)

    call([
        'k8s-migration', 'vars', 'fetch-repo', '-s', service, '-r', repo,
        '-t', GITHUB_TOKEN, '-o', f'{service}.json'
    ])

    call([
        'k8s-migration', 'vars', 'upload', '-c', cluster, '-d', domain,
        '-i', f'{service}.json', '-t', admiral_token, '-r', region, '-u', admiral_url
    ])

    call(['rm', f'{service}.json'])


if __name__ == '__main__':
    main()
