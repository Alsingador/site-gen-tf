import unittest

from main import *


class TestMainSuportFunctions(unittest.TestCase):
    def test_extract_title(self):
        md = "# Yes"
        header = extract_title(md)
        self.assertEqual(header, "Yes")
        md = """
#               Yes
filler
"""
        header = extract_title(md)
        self.assertEqual(header, "Yes")
        md = """
pre filler
# Yes
filler
"""
        header = extract_title(md)
        self.assertEqual(header, "Yes")
        md = """
## No
filler
"""
        with self.assertRaises(Exception):
            header = extract_title(md)
        md = """
 No
filler
"""
        with self.assertRaises(Exception):
            header = extract_title(md)
        md = """
#No
filler
"""
        with self.assertRaises(Exception):
            header = extract_title(md)
