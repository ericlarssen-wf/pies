import logging

import boto3
import click
import click_log
from github import Github
import yaml

import k8s_migration
from k8s_migration.admiral import AdmiralClient
from k8s_migration import aws
from k8s_migration import migrate

logger = logging.getLogger(__name__)

KEY_ID = 'alias/WorkivaDeployEncryptionKey'
PARAM_PREFIX = '/workiva-deploy/kubernetes'
ADMIRAL_URL = 'https://admiral.wk-dev.workiva.org/'
ADMIRAL_TOKEN = ''
GITHUB_TOKEN = ''

@click.command()
@click.pass_context
@click_log.init(logger)
@click.version_option(k8s_migration.__version__, message='%(version)s')
@click.option('-s', '--service', required=True)
@click.option('-r', '--repo', required=True)
@click.option('-c', '--cluster', required=True)
@click.option('-k', '--kms-region', default='us-east-1')
def main(ctx, service, repo, cluster, kms_region):
    ctx.obj={}
    ctx.obj['SERVICE'] = service
    ctx.obj['CLUSTER'] = cluster
    ctx.obj['KMS_REGION'] = kms_region

    aws_client = boto3.client('ssm')
    set_parameters = aws.get_parameters(aws_client, cluster, service)

    # Fetch values.yaml content from Repo.
    github_client = Github(GITHUB_TOKEN)
    org = github_client.get_organization('Workiva')
    repo = org.get_repo(repo)
    values = repo.get_file_contents('/helm/{}/values.yaml'.format(service))
    values_data = yaml.load(values.decoded_content)
    print values_data

    # Fetch latest deploy from Admiral
    admiral_client = AdmiralClient(ADMIRAL_URL, ADMIRAL_TOKEN)
    response = admiral_client.get_deploys(service)
    latest_deploy = next(d for d in response['deploys'] if d['active'])
    container = latest_deploy['containers'][0]
    print latest_deploy

    # TODO determine cluster domain based on clusters
    # write_parameter(ctx, key, value, is_secret=False)

    if values_data.get('iamRole'):
        if not latest_deploy.get('iam_role_arn'):
            if click.confirm('Unable to find an iam_role_arn, would you like to provide one at this time?', default=False):
                iam_role_arn = click.prompt('Enter a valid iam_role_arn', default=None)

        logger.info('Writing iamRole to Parameter Store.')
        aws.write_parameter(client, cluster, service, key, value, is_secret=False)

    if not values_data.get('environment'):
        logger.info('No environment variables to set in values.yaml')
    else:
        for key, value in values_data['environment']:
            is_set = 'environment.{}'.format(key) in set_parameters:

            force = False
            if value:
                if is_set:
                    if click.confirm('Parameter, {} already exists, but now has a default in the values.yaml. Would you like to delete it?'.format(key), default=False):
                        logger.info('Deleting {}...'.format(key))

                continue

            if not container['environment'].get(key):
                if click.confirm('Unable to find {}, would you like to provide one at this time?'.format(key), default=False):
                    value = click.prompt('Enter a valid {}'.format(key), default=None)

            if is_set:
                if click.confirm('Parameter, {}, already exists, would you like to overwrite it?'.format(key), default=False):
                    force = True
                else:
                    logger.info('Skipping {}...'.format(key))
                    continue

            logger.info('Writing {}={} to Parameter Store.'.format(key, value))
            aws.write_parameter(cluster, client, service, 'environment.{}'.format(key), value, force=force)

    if not values_data.get('secrets'):
        logger.info('No secret variables to set in values.yaml')
    else:
        for key, value in values_data['secrets']:
            if value:
                logger.info('{} is defaulted in the values yaml. Inform the team they should not have defaults for secrets.'.format(key))
                continue

            if not container['environment'].get(key):
                if click.confirm('Unable to find {}, would you like to provide one at this time?', default=False):
                    value = click.prompt('Enter a valid {}'.format(key), default=None)

            if 'secrets.{}'.format(key) in set_parameters:
                if click.confirm('Parameter, {}, already exists, would you like to overwrite it?'.format(key), default=False):
                    force = True
                else:
                    logger.info('Skipping {}...'.format(key))
                    continue

            logger.info('Writing secret {}={} to Parameter Store.'.format(key, value))
            aws.write_parameter(cluster, client, service, 'secrets.{}'.format(key), value, force=force)
