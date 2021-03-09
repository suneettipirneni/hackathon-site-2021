# flake8: noqa
import json
from src.models.sponsor import Sponsor
from tests.base import BaseTestCase
from src.models.user import ROLES


class TestSponsorsBlueprint(BaseTestCase):
    """Tests for the Sponsors Endpoints"""

    """create_sponsor"""
    def test_create_sponsor(self):
        pass

    def test_create_sponsor_invalid_json(self):
        pass

    def test_create_sponsor_duplicate_sponsor(self):
        pass

    def test_create_sponsor_invalid_datatypes(self):
        pass

    def test_get_sponsor(self):
        Sponsor.createOne(
            username="Simon",
            email="simon@gmail.com",
            password="randomstring",
            sponsor_name="SimonCorp",
            roles=ROLES.SPONSOR
        )
        
        res = self.client.get("/api/sponsor/SimonCorp/")

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 200)
        self.assertTrue("username" in data)
