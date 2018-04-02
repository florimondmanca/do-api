"""Functional API tests."""

import pytest

from falcon.testing import TestClient as Client


def test_list_lists_empty_db(client: Client):
    result = client.simulate_get('/lists')
    assert result.status_code == 200, result.json
    assert result.json == []


def test_create_list_without_title_bad_request(client: Client, list_title):
    result = client.simulate_post('/lists', json={})
    assert result.status_code == 400


def test_create_list(client: Client, list_title):
    payload = {
        'title': list_title,
    }
    result = client.simulate_post('/lists', json=payload)
    assert result.status_code == 201
    assert result.json == {
        'id': 1,
        'title': list_title,
        'archived': False,
        'tasks': [],
    }


def test_list_lists(client: Client, list_title):
    result = client.simulate_get('/lists')
    assert result.status_code == 200, result.json
    assert result.json == [
        {
            'id': 1,
            'title': list_title,
            'archived': False,
        },
    ]


def test_list_detail(client: Client, list_title):
    result = client.simulate_get('/lists/1')
    assert result.status_code == 200, result.json
    assert result.json == {
        'id': 1,
        'title': list_title,
        'archived': False,
        'tasks': [],
    }


task_defaults = {
    'due_date': None,
    'completed': False,
    'priority': 0,
}


@pytest.mark.parametrize('omitted, id', [
    (None, 1), ('due_date', 2), ('completed', 3), ('priority', 4),
])
def test_create_task(client: Client, task_payload, omitted, id):
    expected = {**task_payload, 'id': id}
    if omitted:
        task_payload.pop(omitted)
        expected[omitted] = task_defaults[omitted]

    result = client.simulate_post('/tasks', json=task_payload)
    assert result.status_code == 201, result.json
    assert result.json == expected


@pytest.mark.parametrize('key, value', [
    (None, None),
    ('completed', True),
    ('due_date', None),
    ('priority', 3),
])
def test_update_task(client: Client, now, key, value):
    if key == 'due_date':
        value = str(now)
    payload = key and {key: value} or {}
    result = client.simulate_patch('/tasks/1', json=payload)
    assert result.status_code == 200, result.json
    if key:
        assert result.json[key] == value


def test_delete_task(client: Client):
    result = client.simulate_delete('/tasks/1')
    assert result.status_code == 204


def test_deleted_task_not_in_list_anymore(client: Client):
    result = client.simulate_get('/lists/1')
    assert result.status_code == 200
    assert 1 not in [task['id'] for task in result.json['tasks']]


def test_delete_list(client: Client):
    result = client.simulate_delete('/lists/1')
    assert result.status_code == 204


def test_deleted_list_not_found(client: Client):
    result = client.simulate_get('/lists/1')
    assert result.status_code == 404


@pytest.mark.parametrize('resource', ['tasks', 'lists'])
def test_delete_task_or_list_not_found(client: Client, resource):
    result = client.simulate_delete('/{}/1'.format(resource))
    assert result.status_code == 404


def test_list_detail_not_found(client: Client):
    result = client.simulate_get('/lists/123456789')
    assert result.status_code == 404, result.json


def test_list_detail_non_int_id_not_found(client: Client):
    result = client.simulate_get('/lists/abcd')
    assert result.status_code == 404
