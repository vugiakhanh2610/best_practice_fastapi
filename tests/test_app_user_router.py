import os
import sys

sys.path.append(f'{os.getcwd()}')

from tests.setup_environment import client

PREFIX = '/api/v1'
def test_get_list(client):
    response = client.get(f'{PREFIX}/app_users')
    assert response.status_code == 200
