import logging
import requests

logger = logging.getLogger(__name__)


class AdmiralClient(object):
    """
    Client for interfacing with admiral.
    """

    def __init__(self, url, apikey):

        self.url = url.rstrip('/') + '/'
        self.apikey = apikey

        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-Api-Key': apikey,
        })

    def request(self, method, endpoint, **kwargs):
        """
        Make an HTTP request.
        :param method: The method of the request.
        :param endpoint: The endpoint on the orchestrator for the request.
        :param kwargs: Additional arguments to `requests.request`.
        :return: `requests.Response` object.
        """
        url = '{}api/v1/{}'.format(self.url, endpoint)

        logger.debug('{}: {}'.format(method, url))

        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()

        return response

    def get(self, endpoint, **kwargs):
        """
        Make an HTTP GET request.
        :param endpoint: The endpoint on the orchestrator for the request.
        :param kwargs: Additional arguments to `requests.request`.
        :return: `requests.Response` object.
        """
        return self.request('GET', endpoint, **kwargs)

    def get_deploys(self, service):
        """
        Get deploys.
        :param service: The Admiral service id.
        """
        return self.get('deploys/{}/default'.format(service)).json()

    def download_file(self, file_id):
        """
        Download a file.
        :param file_id: The id of the file to be downloaded.
        """
        return self.get('files/{}'.format(file_id)).content
