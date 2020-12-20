from src.ip_api import get_external_ip
import unittest
import re


class TestIpApi(unittest.TestCase):

    def test_get_external_ip(self):
        self.assertIsNotNone(
            re.match(
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
                get_external_ip()
            )
        )
