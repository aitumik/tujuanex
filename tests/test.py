from datetime import datetime,timedelta
import unittest
from ..app import db
from app.tujuanex.models import User,Post

class UserModelCase(TestCase):
    def setUp(self):
        #db.create_all()
        pass

    def tearDown(self):
        pass

    def test_avatar(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)

