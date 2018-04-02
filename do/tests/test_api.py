"""Functional API tests."""

from falcon.testing import TestClient as Client
from models import List


def test_lists_list_empty_db(session, client: Client):
    result = client.simulate_get('/lists')
    assert result.status_code == 200
    assert result.json == []


def test_lists_list(session, client: Client):
    list_ = List(title='test')
    session.add(list_)
    session.commit()

    result = client.simulate_get('/lists')
    assert result.status_code == 200
    assert result.json == [
        {
            'id': 1,
            'title': 'test',
            'archived': False,
        }
    ]


def test_list_detail(client: Client):
    result = client.simulate_get('/lists/1')
    assert result.status_code == 200
    assert result.json == {
        'id': 1,
        'title': 'test',
        'archived': False,
        'tasks': [],
    }


def test_list_detail_not_found(session, client: Client):
    result = client.simulate_get('/lists/123456789')
    assert result.status_code == 404


def test_list_detail_non_int_id_not_found(client: Client):
    result = client.simulate_get('/lists/abcd')
    assert result.status_code == 404
