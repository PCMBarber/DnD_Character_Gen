from application import db, login_manager
from flask_login import UserMixin

class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    char_name = db.Column(db.String(30), nullable=False, unique=True)
    race = db.Column(db.String(30), nullable=False)
    char_class = db.Column(db.String(30), nullable=False)
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    background = db.Column(db.String(30), nullable=False)
    feats = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return ''.join(['Char ID: ', str(self.id), '\r\n',
            'Name: ', self.char_name, '\r\n',
            'race: ', self.race, '\r\n',
            'class: ', self.char_class, '\r\n',
            'strength: ', str(self.strength), '\r\n',
            'dexterity: ', str(self.dexterity), '\r\n',
            'constitution: ', str(self.constitution), '\r\n',
            'intelligence: ', str(self.intelligence), '\r\n',
            'wisdom: ', str(self.wisdom), '\r\n',
            'charisma: ', str(self.charisma), '\r\n',
            'background: ', self.background, '\r\n',
            'feat list: ', self.feats
        ])
    
    @login_manager.user_loader
    def load_user(id):
        return user.query.get(int(id))

class feat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    effects = db.Column(db.String(300), nullable=False)
    skillmodify = db.Column(db.String(30))
