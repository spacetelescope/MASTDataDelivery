"""
.. module:: _test_deliver_data

   :synopsis: Test module for deliver_data.py

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import os
import deliver_data
import unittest

#--------------------

class TestGetDataKepler(unittest.TestCase):
    """ Main test class. """
    reference_file_path = "unit_test_reffiles/deliver_data/"

    def testCase01(self):
        """ This uses Kepler 16 to test Kepler long cadence. """
        new_str = deliver_data.deliver_data(
            ["kepler"], ["kplr012644769_lc_Q111111111111111111"])
        old_file = self.reference_file_path + "test_case_01.txt"
        if os.path.isfile(old_file):
            with open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def testCase02(self):
        """ This uses KIC 757450 to test Kepler short cadence. """
        new_str = deliver_data.deliver_data(
            ["kepler"], ["kplr000757450_sc_Q000000000033333300"])
        old_file = self.reference_file_path + "test_case_02.txt"
        if os.path.isfile(old_file):
            with open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def testCase03(self):
        """ This uses both Kepler 16 and KIC 757450 to test more than one obsID
        in a single request.  It also includes a mix of cadence types. """
        new_str = deliver_data.deliver_data(
            ["kepler", "kepler"],
            ["kplr012644769_lc_Q111111111111111111",
             "kplr000757450_sc_Q000000000033333300"])
        old_file = self.reference_file_path + "test_case_03.txt"
        if os.path.isfile(old_file):
            with open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

#--------------------

if __name__ == "__main__":
    unittest.main()

