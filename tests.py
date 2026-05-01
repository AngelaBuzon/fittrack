import pytest
from app import create_app, db
from app.models import Usuario

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_pagina_login(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_pagina_registro(client):
    response = client.get('/registro')
    assert response.status_code == 200

def test_registro_usuario(client):
    response = client.post('/registro', data={
        'nombre': 'Test',
        'email': 'test@test.com',
        'password': '1234'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_incorrecto(client):
    response = client.post('/login', data={
        'email': 'noexiste@test.com',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_dashboard_sin_login(client):
    response = client.get('/dashboard/', follow_redirects=True)
    assert response.status_code == 200

def test_musculacion_sin_login(client):
    response = client.get('/musculacion/', follow_redirects=True)
    assert response.status_code == 200

def test_rutas_sin_login(client):
    response = client.get('/rutas/', follow_redirects=True)
    assert response.status_code == 200