# tools/create_admin.py
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()
with app.app_context():
    if not User.query.filter_by(email="admin@example.com").first():
        u = User(email="admin@example.com", name="Admin", is_admin=True)
        u.set_password("password123")
        db.session.add(u)
        db.session.commit()
        print("Created admin user: admin@example.com / password123")
    else:
        print("Admin user already exists.")