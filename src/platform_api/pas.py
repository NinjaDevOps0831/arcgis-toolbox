import requests

from .. import config


def login(username: str, password: str):
    loginUrl = "{}/api/pas/login".format(config.baseUrl)
    return requests.post(
        url=loginUrl,
        data={"grant_type": "password", "username": username, "password": password},
    )
