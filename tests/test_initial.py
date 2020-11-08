from datetime import datetime,timedelta
import unittest
from app import current_app,db
from app.tujuanex.models import User,Post

class UserModelCase(TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

