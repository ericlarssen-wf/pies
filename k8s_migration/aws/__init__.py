def get_parameters(client, cluster, service):
    path = '{}/{}/{}'.format(PARAM_PREFIX, cluster, service)
    response = client.get_parameters_by_path(Path=path, Recursive=True)

    return [p['Name'].split('/')[5] for p in response['Parameters']]


def write_parameter(client, cluster, service, key, value, is_secret=True, force=False):
    name = '{}/{}/{}/{}'.format(PARAM_PREFIX, cluster, service, key)
    type = 'SecureString' if is_secret else 'String'
    client.put_parameter(Name=name, Value=value, Type=type, KeyId=KEY_ID, Overwrite=force)


def delete_parameter(client, cluster, service, key):
    name = '{}/{}/{}/{}'.format(PARAM_PREFIX, cluster, service, key)
    client.delete_parameter(Name='name')
