"""Tests use a real MySQL database configured through .env/environment variables.
They create their own rows and delete only those rows after each test.
"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from app import app, database

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def payload():
    return dict(title='Test: Research for sustainable farming', description='Analyze crop imagery with a faculty research team.', research_area='Artificial Intelligence', faculty_name='Dr. Test Faculty', department='Computer Science', required_skills='Python, machine learning', available_positions=2, application_deadline='2027-01-31', status='Open')

@pytest.fixture
def created(client, payload):
    ids = []
    def create(data=None):
        response = client.post('/api/opportunities', json=data or payload)
        assert response.status_code == 201
        row = response.get_json()['data']
        ids.append(row['id'])
        return row
    yield create
    with database() as connection, connection.cursor() as cursor:
        for opportunity_id in ids:
            cursor.execute('DELETE FROM opportunities WHERE id=%s', (opportunity_id,))

def test_full_crud_and_status(client, created):
    row = created()
    path = f"/api/opportunities/{row['id']}"
    assert client.get(path).get_json()['data']['title'] == row['title']
    assert row['id'] in [item['id'] for item in client.get('/api/opportunities').get_json()['data']]
    updated = client.put(path, json={'title': 'Updated title', 'available_positions': 3})
    assert updated.status_code == 200
    assert updated.get_json()['data']['available_positions'] == 3
    assert client.put(path, json={'status':'Closed'}).get_json()['data']['status'] == 'Closed'
    assert client.get(path).get_json()['data']['status'] == 'Closed'
    assert client.delete(path).status_code == 200
    assert client.get(path).status_code == 404
    assert client.put(path, json={'status':'Open'}).status_code == 404
    assert client.delete(path).status_code == 404

@pytest.mark.parametrize('field,value', [('title',' '),('description',''),('available_positions',0),('available_positions',True),('available_positions',1.5),('available_positions','2'),('available_positions',10001),('application_deadline','2027-02-30'),('application_deadline','tomorrow'),('application_deadline','2027-W01-1'),('status','Pending'),('title','a'*201),('unexpected','x')])
def test_invalid_values(client,payload,field,value):
    payload[field] = value
    result = client.post('/api/opportunities',json=payload)
    assert result.status_code == 400
    assert result.get_json()['errors']

@pytest.mark.parametrize('field', ['title','description','research_area','faculty_name','department','required_skills','available_positions','application_deadline'])
def test_missing_fields(client,payload,field):
    del payload[field]
    assert client.post('/api/opportunities',json=payload).status_code == 400

def test_default_status_and_location(client,payload,created):
    del payload['status']
    row = created(payload)
    assert row['status'] == 'Open'

def test_bad_body_and_unknown_route(client,created):
    assert client.post('/api/opportunities',data='{bad',content_type='application/json').status_code == 400
    assert client.post('/api/opportunities',json=[]).status_code == 400
    row = created()
    assert client.put(f"/api/opportunities/{row['id']}",json={}).status_code == 400
    assert client.get('/api/opportunities/not-a-number').status_code == 404

def test_invalid_update_is_not_saved(client,created):
    row = created()
    path = f"/api/opportunities/{row['id']}"
    assert client.put(path,json={'title':'','status':'Closed'}).status_code == 400
    unchanged = client.get(path).get_json()['data']
    assert unchanged['title'] == row['title']
    assert unchanged['status'] == 'Open'

def test_sql_like_text_is_stored_as_text(client,payload,created):
    payload['title'] = "Robert'); DROP TABLE opportunities; --"
    row = created(payload)
    assert client.get(f"/api/opportunities/{row['id']}").get_json()['data']['title'] == payload['title']
    assert client.get('/api/opportunities').status_code == 200

def test_database_failure_is_json_500(client,monkeypatch):
    def fail():
        raise RuntimeError('test failure; never exposed to the client')
    monkeypatch.setattr('app.database',fail)
    response = client.get('/api/opportunities')
    assert response.status_code == 500
    assert response.is_json
    assert 'never exposed' not in response.get_data(as_text=True)

def test_frontend_and_health(client):
    assert client.get('/').status_code == 200
    assert client.get('/assets/app.js').status_code == 200
    assert client.get('/api/health').get_json()['database'] == 'MySQL'

