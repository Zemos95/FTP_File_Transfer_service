from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password  # In der Produktion sollten Passwörter gehasht werden

    # Optional: Implementieren Sie weitere Methoden oder Attribute nach Bedarf