import io
import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from extensions import db
from models import User, Document, Permission


@pytest.fixture
def app(tmp_path):
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(tmp_path / "test.db"),
        "UPLOAD_FOLDER": str(tmp_path / "uploads"),
        "SECRET_KEY": "test-secret",
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
        owner = User(username="owner1", email="owner@example.com",
                     password_hash=generate_password_hash("password123"), role="owner")
        viewer = User(username="viewer1", email="viewer@example.com",
                      password_hash=generate_password_hash("password123"), role="owner")
        db.session.add_all([owner, viewer])
        db.session.commit()
        doc = Document(original_name="private.txt", stored_name="private.txt",
                       file_size=6, owner_id=owner.id)
        db.session.add(doc)
        db.session.commit()
        with open(app.config["UPLOAD_FOLDER"] + "/private.txt", "wb") as f:
            f.write(b"secret")
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_unshared_user_cannot_download(app):
    client = app.test_client()
    client.post("/login", data={"identity": "viewer1", "password": "password123"})
    response = client.get("/documents/1/download")
    assert response.status_code == 403


def test_shared_read_user_can_download(app):
    with app.app_context():
        viewer = User.query.filter_by(username="viewer1").first()
        db.session.add(Permission(user_id=viewer.id, document_id=1,
                                  can_read=True, can_edit=False, granted_by=1))
        db.session.commit()
    client = app.test_client()
    client.post("/login", data={"identity": "viewer1", "password": "password123"})
    response = client.get("/documents/1/download")
    assert response.status_code == 200
    assert response.data == b"secret"


def test_non_owner_cannot_delete(app):
    client = app.test_client()
    client.post("/login", data={"identity": "viewer1", "password": "password123"})
    response = client.post("/documents/1/delete")
    assert response.status_code == 403
