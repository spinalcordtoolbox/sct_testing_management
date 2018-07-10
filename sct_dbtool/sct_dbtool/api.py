import requests
import requests.auth as auth

from typing import List, Dict


class APIClient(object):
    """The API client for the web management tool. This API client
    contains code only for retrieving the entire JSON dataset.

    :param user: username for the web management.
    :param password: password for the web management.
    :param hostname: the hostname for the web management.
    :param port: the port of the web management.
    """
    JSON_URL = "http://{}:{}/annotations/v1/api/datasets/"

    def __init__(self, user: str, password: str,
                 hostname='tristano.neuro.polymtl.ca', port=80):
        self.hostname = hostname
        self.port = port
        self.http_auth = auth.HTTPBasicAuth(username=user,
                                            password=password)

    @classmethod
    def from_config(cls, config: Dict):
        """Use this class method to create a new API client
        from a configuration dictionary.

        :param config: the configuration.
        :return: a new configured APIClient instance.
        """
        return cls(user=config["username"],
                   password=config["password"],
                   hostname=config["hostname"],
                   port=config.getint("port"))

    def get_dataset(self) -> List[Dict]:
        """Retrieves the entire dataset from the server.
                
        :return: list of items from the dataset.
        """
        url = APIClient.JSON_URL.format(self.hostname, self.port)
        response = requests.get(url, auth=self.http_auth)
        if response.status_code != 200:
            raise RuntimeError("Error while retrieving the dataset, "
                               "HTTP code: {}".format(response.status_code))
        dataset = response.json()
        return dataset
