from models import User, Professional
from extensions import db
from werkzeug.security import generate_password_hash
from secrets import token_urlsafe

class SeedProfessionalsService:
    def execute(self):
        for name, email, specialty in [('Studio Alpha', 'alpha@demo.invalid', 'Barbearia'), ('Leandro Silva', 'leandro@demo.invalid', 'Visagismo'), ('Beleza & Estilo', 'beleza@demo.invalid', 'Coloração')]:
            if not User.query.filter_by(email=email).first():
                user = User(name=name, email=email, password_hash=generate_password_hash(token_urlsafe(40)), role='professional').salvar()
                Professional(user_id=user.id, studio_name=name, specialty=specialty, duration_minutes=60).salvar()
        db.session.commit()
