import pytest


@pytest.mark.active
def test_ping(test_app):
    response = test_app.get('/ping')
    print('\ntest_ping\n',
          'response ->', response, '\n',
          )
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
