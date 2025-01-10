from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id: int, username: str, password: str):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    def get_id(self) -> str:
        return str(self.id)

# Dummy-Benutzer (in der Produktion sollten Benutzer in einer Datenbank gespeichert werden)
users = {
    'admin': User(id=1, username='admin', password='password')
}