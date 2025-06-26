from app import create_app, db
from app.models import Message
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    print("Database created.")


with app.app_context():
    username = 'admin'
    password = 'password123'
    hashed_pw = generate_password_hash(password)

    if not User.query.filter_by(username=username).first():
        admin = User(username=username, password=hashed_pw)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin already exists.")