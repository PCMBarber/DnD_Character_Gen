import unittest

from flask import url_for
from flask_testing import TestCase
from os import getenv
from application import app, db
from application.models import user, feat


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('MYSQL_USER'))+':'+str(getenv('MYSQL_PWD'))+'@'+str(getenv('MYSQL_IP'))+'/testDnD'     
            )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test user
        new_user = user(
            char_name="test",
            race="Human",
            char_class="useless",
            strength=1,
            dexterity=2,
            constitution=3,
            intelligence=4,
            wisdom=5,
            charisma=6,
            background="Urchin",
            feats=8,
            password="test"
        )

        new_feat = feat(id=1, name="test feat", effects="Doesn't really matter at the end of the day, does it?")

        db.session.add(new_user)
        db.session.add(new_feat)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestRouting(TestBase):

    def testLogin(self):
        response = self.client.get(url_for('login', char_name="test"))

        self.assertEqual(response.status_code, 200)

    def testHome(self):
        response = self.client.get(url_for('home'))

        self.assertEqual(response.status_code, 200)
    
    def testnew_char(self):
        response = self.client.get(url_for('new_char'))

        self.assertEqual(response.status_code, 200)

    def testnew_char2(self):
        response = self.client.get(url_for('new_char2', char_name="test", race="fluid", char_class="Pigmy"))

        self.assertEqual(response.status_code, 200)

    def testFeats(self):
        response = self.client.get(url_for('feats', char_name="test", race="fluid", char_class="Pigmy", strength=1, dexterity=1, constitution=1, intelligence=1, wisdom=1, charisma=1))

        self.assertEqual(response.status_code, 200)
    
class TestModels(TestBase):
    
    def test_user_model(self):
        new_user2 = user(
            char_name="test2",
            race="Human",
            char_class="useless",
            strength=1,
            dexterity=2,
            constitution=3,
            intelligence=4,
            wisdom=5,
            charisma=6,
            background="Urchin",
            feats=8,
            password="test"
        )

        db.session.add(new_user2)
        db.session.commit()

        self.assertEqual(user.query.count(), 2)
    
    def test_feat_model(self):
        new_feat2 = feat(id=2, name="test feat2", effects="You are a very fine person, Mr. Baggins, and I am very fond of you; but you are only quite a little fellow in a wide world after all! 'Thank goodness!' said Bilbo laughing, and handed him the tobacco jar.")

        db.session.add(new_feat2)
        db.session.commit()

        self.assertEqual(feat.query.count(), 2)

