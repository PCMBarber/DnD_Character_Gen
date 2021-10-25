from wtforms import StringField, SubmitField, IntegerField, PasswordField, SelectField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import user, feat
from application import login_manager, password_hash as pw

class LoginForm(FlaskForm):
    password = PasswordField('Password: ',
        validators=[DataRequired(message=None)
        ]    
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class NewChar1(FlaskForm):
    char_name = StringField('Character name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    race = SelectField(
        'Race: ',
        choices=[            
            ('Human','Human'), 
            ('Elf','Elf'), 
            ('Dwarf','Dwarf'), 
            ('Halfling','Halfling'), 
            ('Gnome','Gnome'), 
            ('Half-Orc','Half-Orc'),
            ('Tiefling','Tiefling')
        ]
    )
    char_class = SelectField(
        'Class: ',
        choices=[
            ('Fighter','Fighter'),
            ('Wizard','Wizard'),
            ('Cleric','Cleric'),
            ('Rogue','Rogue'),
            ('Ranger','Ranger')
        ]
    )
    submit = SubmitField('Confirm')

class NewChar2(FlaskForm):
    strength = SelectField(
        'Strength: ',
        choices=[
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6')
        ]
    )
    dexterity = SelectField(
        'Dexterity: ',
        choices=[
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6')
        ]
    )
    constitution = SelectField(
        'Constitution: ',
        choices=[
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6')
        ]
    )
    intelligence = SelectField(
        'Intelligence: ',
        choices=[
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6')
        ]
    )
    wisdom = SelectField(
        'Wisdom: ',
        choices=[
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6')
        ]
    )
    charisma = SelectField(
        'Charisma: ',
        choices=[
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6')
        ]
    )
    submit = SubmitField('Confirm')

    def validate(self):
        result = True
        seen = set()
        for field in [self.strength, self.dexterity, self.constitution, 
            self.intelligence, self.wisdom, self.charisma]:
            if field.data in seen:
                errors=list(field.errors)
                errors.append('Please select six different numbers')
                field.errors=tuple(errors)
                result = False
            else:
                seen.add(field.data)
        return result

class PasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', 
        validators=[DataRequired()
        ]
    )
    password = PasswordField('Password', 
        validators=[DataRequired()
        ]
    )
    confirm_pass = PasswordField('Password', 
        validators=[DataRequired(), 
            EqualTo('password')
        ]
    )
    submit = SubmitField('Confirm Password')

class CreatePasswordForm(FlaskForm):
    password = PasswordField('Password', 
        validators=[DataRequired()
        ]
    )
    confirm_password = PasswordField('Confirm password', 
        validators=[DataRequired(), 
            EqualTo('password')
        ]
    )
    submit = SubmitField('Confirm Password')