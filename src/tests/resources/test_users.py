import json
import pytest
from httpx import AsyncClient
# from asgi_lifespan import LifespanManager
from src.api.crud import user_crud
# from src.api.sqlalchemy_models import models


@pytest.mark.asyncio
# @pytest.mark.active
async def test_users_read_users(mocker, async_test_client: AsyncClient):
    expected_response_json = [
        {
            "email": "1@test.com",
            "id": 1,
            "is_active": True,
            "items": [
                {
                    "title": "title 1",
                    "description": "secription 1",
                    "id": 1,
                    "owner_id": 1
                }
            ]
        },
        {
            "email": "2@test.com",
            "id": 2,
            "is_active": True,
            "items": [
                {
                    "title": "title 2",
                    "description": "secription 2",
                    "id": 2,
                    "owner_id": 2
                }
            ]
        }

    ]
    mocker.patch('src.api.crud.user_crud.get_users',
                 return_value=expected_response_json)

    response = await async_test_client.get('/users/')
    # print('\ntest_users_read_users\n',
    #       'response.json ->', response.json(), '\n',
    #       )
    assert response.json() == expected_response_json


@pytest.mark.asyncio
@pytest.mark.active
async def test_users_read_user(mocker, async_test_client: AsyncClient):
    user_id = 3
    return_value = {
        'email': '3@test.com',
        'id': 3,
        'is_active': True,
        'items': [{
            'title': 'title 3',
            'description': 'secription 3',
            'id': 3,
            'owner_id': 3}]
        }
    mocker.patch(
        'src.api.crud.user_crud.get_user',
        return_value=return_value
    )
    spy_on_get_user = mocker.spy(user_crud, 'get_user')

    response = await async_test_client.get(f'/users/{user_id}')

    _, kargs = spy_on_get_user.call_args

    assert kargs == {'user_id': user_id}

    mocker.patch(
        'src.api.crud.user_crud.get_user',
        return_value=None
    )

    response = await async_test_client.get(f'/users/{user_id}')

    _, kargs = spy_on_get_user.call_args

    assert kargs == {'user_id': user_id}
    assert response.status_code == 404
    assert response.json().get('detail') == 'User not found'

    # print('\ntest_users_read_users\n',
    #       'response.json ->', response.json(), '\n',
    #       'kargs ->', kargs, '\n',
    #       )


@pytest.mark.asyncio
# @pytest.mark.active
async def test_users_create_user_sucsess(
        mocker, async_test_client: AsyncClient):

    args_create_user = {"email": "mock_email", "password": "mock_password"}
    expected_response = {
        'email': args_create_user.get('email'),
        'id': 8,
        'is_active': True,
        'items': []
    }

    mocker.patch(
        'src.api.crud.user_crud.get_user_by_email',
        return_value=None
    )
    spy_on_get_user_by_email = mocker.spy(
        user_crud,
        'get_user_by_email'
    )

    mocker.patch(
        'src.api.crud.user_crud.create_user',
        return_value=expected_response)
    spy_on_create_user = mocker.spy(
        user_crud,
        'create_user'
    )

    response = await async_test_client.post(
        '/users/',
        json=args_create_user,
    )
    _, spy_on_get_user_by_email_args = spy_on_get_user_by_email.call_args
    _, spy_on_create_user_args = spy_on_create_user.call_args

    assert spy_on_get_user_by_email.call_count == 1
    assert spy_on_get_user_by_email_args == {
        k: v for (k, v) in args_create_user.items() if k == 'email'}
    assert spy_on_create_user.call_count == 1
    assert spy_on_create_user_args == {'user': args_create_user}
    assert response.json() == expected_response


@pytest.mark.asyncio
# @pytest.mark.active
async def test_users_create_user_fail_already_registered(
        mocker, async_test_client: AsyncClient):

    args_create_user = {"email": "mock_email", "password": "mock_password"}
    expected_response_json = {'detail': 'This email already registered.'}

    mocker.patch(
        'src.api.crud.user_crud.get_user_by_email',
        return_value='Not None'
    )
    spy_on_get_user_by_email = mocker.spy(
        user_crud,
        'get_user_by_email'
    )

    mocker.patch('src.api.crud.user_crud.create_user')
    spy_on_create_user = mocker.spy(
        user_crud,
        'create_user'
    )

    response = await async_test_client.post(
        '/users/',
        json=args_create_user,
    )
    _, spy_on_get_user_by_email_args = spy_on_get_user_by_email.call_args
    # _, spy_on_create_user_args = spy_on_create_user.call_args
    # expected_args = {k: v for (k, v) in args.items() if k == 'email'}

    # _, kargs2 = spy_on_create_user.call_args
    # print('\ntest_users_create_user\n',
    #       'response.json ->', response.status_code, '\n',
    #       'response.json ->', response.json(), '\n',
    #       'spy_on_create_user. ->', spy_on_create_user.call_args, '\n',
    #       )
    assert spy_on_get_user_by_email.call_count == 1
    assert spy_on_get_user_by_email_args == {
        k: v for (k, v) in args_create_user.items() if k == 'email'}
    assert spy_on_create_user.call_count == 0
    assert spy_on_create_user.call_args is None
    assert response.status_code == 400
    assert response.json() == expected_response_json

    # assert spy_on_create_user_args == {'user': args_create_user}
    # assert response.json() == expected_response
