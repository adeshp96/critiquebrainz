import unittest
from flask import Flask
from flask.ext.testing import TestCase
import fixtures
import models
import views
from test_config import db_uri
from utils.converters import FlaskUUID

class AppTestCase(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        FlaskUUID(app)
        views.register_views(app)
        return app

    def setUp(self):
        models.create_tables(self.app)
        fixtures.install(self.app, *fixtures.all_data)
        self.db = models.init_app(self.app)

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_show_publication(self):
        response = self.client.get('/publication/%s' % (fixtures.PublicationData.publication01.id))
        self.assert_200(response)
        
        self.assertEqual(response.json['publication']['id'], fixtures.PublicationData.publication01.id)
        response = self.client.get('/publication/%s' % ('not-valid-uuid'))
        self.assert_404(response)
        
        publication = self.db.session.query(models.Publication).get(fixtures.PublicationData.publication01.id)
        self.db.session.delete(publication)
        self.db.session.commit()
        response = self.client.get('/publication/%s' % (fixtures.PublicationData.publication01.id))
        self.assert_404(response)

if __name__ == '__main__':
    unittest.main()
