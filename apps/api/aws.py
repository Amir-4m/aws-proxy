import boto3

from botocore.config import Config
from django.conf import settings


class AmazonWebServiceAPI(object):
    """
    Contains API and methods that required for connecting and handling AWS servers.
    """

    def __init__(self, name, access_key, secret_key, region):
        self.instance_name = name
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.output = 'json'

    def client(self):
        """
        check client ip address country to be as same as the server ip address location.
        :return: aws client if pass the ip check with succeed status.
        """
        if self.instance_name is None:
            raise ValueError("instance name should not be none!")
        if self.access_key is None:
            raise ValueError("access key should not be none!")
        if self.secret_key is None:
            raise ValueError("secret key should not be none!")
        if self.region is None:
            raise ValueError("region should not be none!")

        if settings.DEVEL:
            raise RuntimeError('your ip address country does not have permission to do this!')
        if not settings.AWS_PROXY:
            config = Config(
                region_name=self.region,
            )
        else:
            config = Config(
                region_name=self.region,
                proxies={
                    'http': f'http://{settings.AWS_PROXY}',
                    'https': f'https://{settings.AWS_PROXY}'
                }

            )

        return boto3.client(
            'lightsail',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=config
        )

    def stop_server(self):
        """
        request aws api to stop the server.

        :return: json returned from response that shows the operation info.
        """
        try:
            response = self.client().stop_instance(instanceName=self.instance_name, force=False)
        except Exception as e:
            raise e
        return response

    def start_server(self):
        """
        request aws api to start the server.

        :return: json returned from response that shows the operation info.
        """
        try:
            response = self.client().start_instance(instanceName=self.instance_name)
        except Exception as e:
            raise e
        return response

    def get_server_ip(self):
        """
        request aws api to get instance(server) current info.

        :return: public ip address of the server.
        """
        try:
            response = self.client().get_instance(instanceName=self.instance_name)
            res = response['instance']['publicIpAddress']
        except KeyError:
            response = self.client().get_instance(instanceName=self.instance_name)
            res = response['instance']['publicIpAddress']
        except Exception as e:
            raise e
        return res

    def get_server_state(self):
        """
        request aws api to get instance(server) current info.

        :return: public ip address of the server.
        """
        try:
            response = self.client().get_instance(instanceName=self.instance_name)
            res = response['instance']['state']['name']
        except Exception as e:
            raise e
        return res
