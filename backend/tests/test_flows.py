from datetime import datetime, timedelta, timezone
import pytest
from extensions import db
from models import FacialAnalysis, HairHistory, Appointment, Simulation

ANALYSIS = dict(face_shape='oval', hair_type='curly', current_length='medium', observations='Teste de integração')
HISTORY = dict(procedure_type='Corte', procedure_date='2026-01-01', next_maintenance_date='2026-02-01', description='Corte curto')

def create(client, auth, resource, data):
    r = client.post('/api/'+resource, headers=auth, json=data)
    assert r.status_code == 201, r.json
    return r.json


def test_registration_login_and_profile(client, auth):
    assert client.get('/api/profile').status_code == 401
    assert client.post('/api/auth/login', json={'email':'aluno@example.com','password':'errada123'}).status_code == 401
    r=client.post('/api/auth/login', json={'email':'aluno@example.com','password':'Teste12345'})
    assert r.status_code == 200 and 'password_hash' not in r.json['user']
    assert client.post('/api/auth/register', json={'name':'X','email':'aluno@example.com','password':'Teste12345'}).status_code == 409
    r=client.put('/api/profile', headers=auth, json={'name':'Nome atualizado','phone':'31999990000','birth_date':'2006-06-03'})
    assert r.status_code == 200
    assert client.get('/api/profile',headers=auth).json['name']=='Nome atualizado'
    r=client.put('/api/preferences',headers=auth,json={'hair_type':'curly','hair_length':'short'})
    assert r.status_code==200
    assert client.get('/api/preferences',headers=auth).json['hair_length']=='short'
    assert client.put('/api/preferences',headers=auth,json={'hair_type':'invalid','hair_length':'short'}).status_code==400

@pytest.mark.parametrize('resource,model,data,change',[
 ('analyses',FacialAnalysis,ANALYSIS,{'observations':'Alterado'}),
 ('history',HairHistory,HISTORY,{'description':'Alterado'}),
 ('appointments',Appointment,{}, {'notes':'Alterado'}),
 ('simulations',Simulation,{}, {'before_image_url':'https://example.com/before.png'}),
])
def test_complete_crud_with_database(client,auth,app,resource,model,data,change):
    data=dict(data)
    if resource=='appointments':
        professionals=client.get('/api/appointments/professionals',headers=auth).json
        data=dict(professional_id=professionals[0]['id'],appointment_date=(datetime.now(timezone.utc)+timedelta(days=5)).isoformat(),service_name='Visagismo')
    if resource=='simulations':
        data={'analysis_id':create(client,auth,'analyses',ANALYSIS)['id']}
    item=create(client,auth,resource,data)
    item_id=item['id']
    with app.app_context():
        assert db.session.get(model,item_id) is not None
    assert any(x['id']==item_id for x in client.get('/api/'+resource,headers=auth).json)
    assert client.get(f'/api/{resource}/{item_id}',headers=auth).status_code==200
    r=client.put(f'/api/{resource}/{item_id}',headers=auth,json=change)
    assert r.status_code==200, r.json
    assert all(r.json[k]==v for k,v in change.items())
    assert client.delete(f'/api/{resource}/{item_id}',headers=auth).status_code==204
    assert client.get(f'/api/{resource}/{item_id}',headers=auth).status_code==404
    with app.app_context():
        assert db.session.get(model,item_id) is None


def test_recommendations_and_cross_user_isolation(client,auth):
    analysis=create(client,auth,'analyses',ANALYSIS)
    recs=create(client,auth,f"recommendations/analysis/{analysis['id']}/generate",{})
    assert len(recs)==4
    assert client.get('/api/recommendations?category=care',headers=auth).json[0]['category']=='care'
    assert client.get('/api/recommendations?analysis_id=oops',headers=auth).status_code==400
    assert client.get('/api/recommendations?category=invalid',headers=auth).status_code==400
    assert client.get(f"/api/recommendations/{recs[0]['id']}",headers=auth).status_code==200
    history=create(client,auth,'history',HISTORY)
    simulation=create(client,auth,'simulations',{'analysis_id':analysis['id'],'recommendation_id':recs[0]['id']})
    appointment=create(client,auth,'appointments',{'professional_id':1,'appointment_date':(datetime.now(timezone.utc)+timedelta(days=8)).isoformat(),'service_name':'Corte'})
    second=client.post('/api/auth/register',json={'name':'Outro','email':'outro@example.com','password':'Teste12345'}).json
    other={'Authorization':'Bearer '+second['token']}
    for resource,item_id in [('analyses',analysis['id']),('recommendations',recs[0]['id']),('history',history['id']),('simulations',simulation['id']),('appointments',appointment['id'])]:
        assert client.get(f'/api/{resource}/{item_id}',headers=other).status_code==404
        if resource!='recommendations':
            assert client.put(f'/api/{resource}/{item_id}',headers=other,json={}).status_code==404
            assert client.delete(f'/api/{resource}/{item_id}',headers=other).status_code==404
        assert client.get('/api/'+resource,headers=other).json==[]
    assert client.post(f"/api/recommendations/analysis/{analysis['id']}/generate",headers=other,json={}).status_code==404
    assert client.post('/api/simulations',headers=other,json={'analysis_id':analysis['id']}).status_code==404
    assert client.post('/api/analyses',headers=other,json={**ANALYSIS,'client_id':analysis['client_id']}).json['client_id']!=analysis['client_id']
    # Regeneração preserva comparação; remove associação à sugestão substituída.
    create(client,auth,f"recommendations/analysis/{analysis['id']}/generate",{})
    assert client.get(f"/api/simulations/{simulation['id']}",headers=auth).json['recommendation_id'] is None
    client.delete(f"/api/analyses/{analysis['id']}",headers=auth)
    assert client.get('/api/recommendations',headers=auth).json==[]
    assert client.get('/api/simulations',headers=auth).json==[]

@pytest.mark.parametrize('data',[
 {**ANALYSIS,'score':'abc'}, {**ANALYSIS,'score':101}, {**ANALYSIS,'face_shape':'invalid'},
 {**ANALYSIS,'image_url':'javascript:alert(1)'}, {**ANALYSIS,'image_url':'http://['}, {**ANALYSIS,'hair_type':[]}, {**ANALYSIS,'observations':['x']},
])
def test_invalid_analysis_does_not_persist(client,auth,data):
    assert client.post('/api/analyses',headers=auth,json=data).status_code==400
    assert client.get('/api/analyses',headers=auth).json==[]


def test_transaction_rollback_and_relationship_validation(client,auth):
    a=create(client,auth,'analyses',ANALYSIS)
    b=create(client,auth,'analyses',ANALYSIS)
    r=create(client,auth,f"recommendations/analysis/{a['id']}/generate",{})[0]
    assert client.post('/api/simulations',headers=auth,json={'analysis_id':b['id'],'recommendation_id':r['id']}).status_code==400
    assert client.put('/api/profile',headers=auth,json={'name':'Não deve salvar','phone':42}).status_code==400
    assert client.get('/api/profile',headers=auth).json['name']=='Aluno'
    assert client.post('/api/history',headers=auth,json={**HISTORY,'next_maintenance_date':'2025-01-01'}).status_code==400
    assert client.post('/api/analyses',headers=auth,json=[]).status_code==400


def test_appointment_conflicts_and_status(client,auth):
    when=datetime.now(timezone.utc)+timedelta(days=3)
    data=dict(professional_id=1,appointment_date=when.isoformat(),service_name='Consulta')
    item=create(client,auth,'appointments',data)
    assert client.post('/api/appointments',headers=auth,json={**data,'appointment_date':(when+timedelta(minutes=30)).isoformat()}).status_code==409
    assert client.put(f"/api/appointments/{item['id']}",headers=auth,json={'status':'completed'}).status_code==400
    assert client.put(f"/api/appointments/{item['id']}",headers=auth,json={'status':'cancelled'}).status_code==200
    create(client,auth,'appointments',data)
    assert client.post('/api/appointments',headers=auth,json={**data,'appointment_date':'2020-01-01T12:00:00Z'}).status_code==400
