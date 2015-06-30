"""
.. module:: _test_deliver_data

   :synopsis: Test module for deliver_data.py

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import deliver_data
import os
import unittest
import gzip

#--------------------

class TestGetDataKepler(unittest.TestCase):
    """ Main test class. """
    reference_file_path = "unit_test_reffiles/deliver_data/"

    def test_case01(self):
        """ This uses Kepler 16 to test Kepler long cadence. """
        new_str = deliver_data.deliver_data(
            ["kepler"], ["kplr012644769_lc_Q111111111111111111"])
        old_file = self.reference_file_path + "test_case_01.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case02(self):
        """ This uses KIC 757450 to test Kepler short cadence. """
        new_str = deliver_data.deliver_data(
            ["kepler"], ["kplr000757450_sc_Q000000000033333300"])
        old_file = self.reference_file_path + "test_case_02.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case03(self):
        """ This uses both Kepler 16 and KIC 757450 to test more than one obsID
        in a single request.  It also includes a mix of cadence types. """
        new_str = deliver_data.deliver_data(
            ["kepler", "kepler"],
            ["kplr012644769_lc_Q111111111111111111",
             "kplr000757450_sc_Q000000000033333300"])
        old_file = self.reference_file_path + "test_case_03.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case04(self):
        """ This uses EPIC 202070161 from Campaign 0. """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2varcat"], ["k2varcat202070161-c00_lc"])
        old_file = self.reference_file_path + "test_case_04.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case05(self):
        """ This uses EPIC 201515470 from Campaign 1. """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2varcat"], ["k2varcat201515470-c01_lc"])
        old_file = self.reference_file_path + "test_case_05.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case06(self):
        """ This uses EPIC 060019819 from the Engineering Campaign (cet). """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2sff"], ["k2sff060019819-cet_lc"])
        old_file = self.reference_file_path + "test_case_06.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case07(self):
        """ This uses EPIC 202071387 from Campaign 0. """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2sff"], ["k2sff202071387-c00_lc"])
        old_file = self.reference_file_path + "test_case_07.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case08(self):
        """ This uses EPIC 204417450 from Campaign 2. """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2sff"], ["k2sff204417450-c02_lc"])
        old_file = self.reference_file_path + "test_case_08.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

#--------------------

if __name__ == "__main__":
    unittest.main()
