from flask import render_template, redirect, url_for, Response, request
import requests
from flask_login import login_user, current_user, logout_user, login_required
from application import app, db, password_hash as pw
from application.forms import LoginForm, NewChar1, NewChar2, PasswordForm, CreatePasswordForm
from application.models import user, feat
import json

@app.route('/')
@app.route('/home')
def home():
    query = user.query.all()
    return render_template('home.html', title='CHANGED', users=query)


@app.route('/login/<char_name>', methods=['GET','POST'])
def login(char_name):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        userfound = user.query.filter_by(char_name=char_name).first()
        if userfound and pw.verify_password(userfound.password, form.password.data):
            login_user(userfound, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('character'))
    return render_template('login.html', title='Login', form=form, character=char_name)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/new_char', methods=['GET','POST'])
def new_char():
    form=NewChar1()

    if form.validate_on_submit():
        char_name=form.char_name.data
        race=form.race.data
        char_class=form.char_class.data
        return redirect(url_for('new_char2', char_name=char_name, race=race, char_class=char_class))

    return render_template('new_char1.html', title='New Character', form=form)

@app.route('/new_char2/<char_name>/<race>/<char_class>', methods=['GET','POST'])
def new_char2(char_name, race, char_class):
    form=NewChar2()
    if form.validate_on_submit():
        print(form.strength.data)
        strength=form.strength.data
        dexterity=form.dexterity.data
        constitution=form.constitution.data
        intelligence=form.intelligence.data
        wisdom=form.wisdom.data
        charisma=form.charisma.data

        return redirect(url_for('feats', char_name=char_name, race=race, char_class=char_class, strength=strength, dexterity=dexterity, constitution=constitution, intelligence=intelligence, wisdom=wisdom, charisma=charisma))
    return render_template('new_char2.html', title='New Character', form=form)


@app.route('/feats/<char_name>/<race>/<char_class>/<strength>/<dexterity>/<constitution>/<intelligence>/<wisdom>/<charisma>')
def feats(char_name, race, char_class, strength, dexterity, constitution, intelligence, wisdom, charisma):
    query = feat.query.all()
    return render_template('feats.html', title='Feats', feats=query, char_name=char_name, race=race, char_class=char_class, strength=strength, dexterity=dexterity, constitution=constitution, intelligence=intelligence, wisdom=wisdom, charisma=charisma)

@app.route('/submit/<feat>/<char_name>/<race>/<char_class>/<strength>/<dexterity>/<constitution>/<intelligence>/<wisdom>/<charisma>', methods=['GET','POST'])
def submit(feat, char_name, race, char_class, strength, dexterity, constitution, intelligence, wisdom, charisma):
    dice=requests.get('http://service1:5001/') #{"1":19,"2":16,"3":10,"4":7,"5":5,"6":4}
    background=requests.get('http://service2:5002/') #{"Background":"Noble"}
    
    skill_dice=dice.json()
    back=background.json()

    die1=skill_dice["1"]
    die2=skill_dice["2"]
    die3=skill_dice["3"]
    die4=skill_dice["4"]
    die5=skill_dice["5"]
    die6=skill_dice["6"]

    char_complete=requests.post('http://backend:5003/', json={"char_name":char_name,"race":race,"char_class":char_class,
        "strength":strength, "dexterity":dexterity,"constitution":constitution,
        "intelligence":intelligence,"wisdom":wisdom,"charisma":charisma,"feats":feat, 
        "1":die1,"2":die2,"3":die3,"4":die4,"5":die5,"6":die6
        })
    char=char_complete.json()
    form = CreatePasswordForm()
    if form.validate_on_submit():
        hashed = pw.hash_password(form.password.data)
        new_user = user(
            char_name=char["char_name"],
            race=char["race"],
            char_class=char["char_class"],
            strength=char["strength"],
            dexterity=char["dexterity"],
            constitution=char["constitution"],
            intelligence=char["intelligence"],
            wisdom=char["wisdom"],
            charisma=char["charisma"],
            background=back["Background"],
            feats=char["feats"],
            password=hashed,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login', char_name=char["char_name"]))
    else:
        return render_template('Password.html', title='Password', form=form)


@app.route('/character', methods=['GET','POST'])
@login_required
def character():
    userfeat=feat.query.filter_by(id=current_user.feats).first()
    return render_template('DisplayChar.html', title=current_user.char_name, user=current_user, feat=userfeat)

@app.route("/change_password", methods=['GET','POST'])
@login_required
def change_password():
	form = PasswordForm()
	if form.validate_on_submit():
		if pw.verify_password(current_user.password, form.current_password.data):
			hash = pw.hash_password(form.password.data)
			current_user.password = hash
			db.session.commit()
			return redirect(url_for('character'))
	else:
		return render_template('change_password.html', title='Change Password', form=form)
