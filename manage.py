# manage.py
from app import create_app
from app.extensions.extensions import db

app = create_app()

with app.app_context():
    db.drop_all()     # Удалит все таблицы (если какие-то остались)
    db.create_all()   # Создаст заново таблицы из моделей