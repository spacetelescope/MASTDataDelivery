"""
.. module:: _test_deliver_data

   :synopsis: Test module for deliver_data.py

.. moduleauthor:: Scott W. Fleming <fleming@stsci.edu>
"""

import gzip
import os
import unittest
import deliver_data

#--------------------

class TestGetDataKepler(unittest.TestCase):
    """ Main test class. """
    reference_file_path = "unit_test_reffiles/deliver_data/"

    # Test Cases 1 - 3 = Kepler

    def test_case01(self):
        """ This uses Kepler 16 to test Kepler long cadence. """
        new_str = deliver_data.deliver_data(
            ["kepler"], ["kplr012644769_lc_Q111111111111111111"],
            filters=["kepler"])
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
            ["kepler"], ["kplr000757450_sc_Q000000000033333300"],
            filters=["kepler"])
        old_file = self.reference_file_path + "test_case_02.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    # You can't plot more than one lightcurve at a time, so turn this off for
    # now (it's broken currently witch caches anyways).
    @unittest.skip("Skipping test of two Kepler lightcurves - unsupported.")
    def test_case03(self):
        """ This uses both Kepler 16 and KIC 757450 to test more than one obsID
        in a single request.  It also includes a mix of cadence types. """
        new_str = deliver_data.deliver_data(
            ["kepler", "kepler"],
            ["kplr012644769_lc_Q111111111111111111",
             "kplr000757450_sc_Q000000000033333300"],
            filters=["kepler", "kepler"])
        old_file = self.reference_file_path + "test_case_03.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    # Test Cases 4 - 5 = HLSP_K2VARCAT

    def test_case04(self):
        """ This uses EPIC 202070161 from Campaign 0. """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2varcat"], ["k2varcat202070161-c00_lc"], filters=["k2"])
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
            ["hlsp_k2varcat"], ["k2varcat201515470-c01_lc"], filters=["k2"])
        old_file = self.reference_file_path + "test_case_05.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    # Test Cases 6 - 8 = HLSP_K2SFF

    def test_case06(self):
        """ This uses EPIC 060019819 from the Engineering Campaign (cet). """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2sff"], ["k2sff060019819-cet_lc"], filters=["k2"])
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
            ["hlsp_k2sff"], ["k2sff202071387-c00_lc"], filters=["k2"])
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
            ["hlsp_k2sff"], ["k2sff204417450-c02_lc"], filters=["k2"])
        old_file = self.reference_file_path + "test_case_08.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    # Test Cases 9 - 17 = IUE

    def test_case09(self):
        """ Test of IUE LWP High Dispersion. """
        new_str = deliver_data.deliver_data(
            ["iue"], ["lwp00501"], filters=["HIGH_DISP"])
        old_file = self.reference_file_path + "test_case_09.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case10(self):
        """ Test of IUE LWP Low Dispersion. """
        new_str = deliver_data.deliver_data(
            ["iue"], ["lwp02572"], filters=["LOW_DISP"])
        old_file = self.reference_file_path + "test_case_10.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case11(self):
        """ Test of IUE LWR Low Dispersion (also is a double aperture). """
        new_str = deliver_data.deliver_data(
            ["iue"], ["lwr01244"], filters=["LOW_DISP"])
        old_file = self.reference_file_path + "test_case_11.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case12(self):
        """ Test of IUE LWR High Dispersion. """
        new_str = deliver_data.deliver_data(
            ["iue"], ["lwr01245"], filters=["HIGH_DISP"])
        old_file = self.reference_file_path + "test_case_12.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case13(self):
        """ Test of IUE SWP Low Dispersion. """
        new_str = deliver_data.deliver_data(
            ["iue"], ["swp01687"], filters=["LOW_DISP"])
        old_file = self.reference_file_path + "test_case_13.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case14(self):
        """ Test of IUE SWP High Dispersion. """
        new_str = deliver_data.deliver_data(
            ["iue"], ["swp01688"], filters=["HIGH_DISP"])
        old_file = self.reference_file_path + "test_case_14.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case15(self):
        """ Test of IUE double dispersion. """
        new_str = deliver_data.deliver_data(
            ["iue"], ["lwp04212"], filters=["HIGH_DISP"])
        old_file = self.reference_file_path + "test_case_15.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case16(self):
        """ Test of IUE double aperture. """
        new_str = deliver_data.deliver_data(
            ["iue"], ["lwp15463"], filters=["LOw_DISP"])
        old_file = self.reference_file_path + "test_case_16.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case17(self):
        """ Test of IUE double dispersion and double aperture. """
        new_str = deliver_data.deliver_data(
            ["iue"], ["swp32470"], filters=["HIGH_DISP"])
        old_file = self.reference_file_path + "test_case_17.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    # Test Case 18 = K2

    def test_case18(self):
        """ Test of K2 extracted lightcurves (from mission). """
        new_str = deliver_data.deliver_data(
            ["k2"], ["ktwo205896873-c03_lc"], filters=["k2"])
        old_file = self.reference_file_path + "test_case_18.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    # Test Cases 19-21 = GALEX

    def test_case19(self):
        """ Test of GALEX 2D spectral image (should return error JSON). """
        new_str = deliver_data.deliver_data(
            ["galex"], ["2518748180271595520"], filters=['NUV'],
            urls=[("galex.stsci.edu/data/GR6/pipe/01-vsn/06051-CDFS_00/g/01-"
                   "main/0001-img/07-try/qa/CDFS_00-xg-int_2color.jpg")])
        old_file = self.reference_file_path + "test_case_19.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case20(self):
        """ Test of GALEX 1D FUV extracted spectrum. """
        new_str = deliver_data.deliver_data(
            ["galex"], ["2518748180274763038"], filters=['FUV'],
            urls=[("galex.stsci.edu/data/GR6/pipe/01-vsn/06051-CDFS_00/g/"
                   "01-main/0001-img/07-try/qa/spjpeg/"
                   "CDFS_00_id021790-xg-gsp_spc.jpeg")])
        old_file = self.reference_file_path + "test_case_20.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case21(self):
        """ Test of GALEX 1D NUV extracted spectrum. """
        new_str = deliver_data.deliver_data(
            ["galex"], ["2505272565762628292"], filters=['NUV'],
            urls=[("galex.stsci.edu/data/GR7/pipe/01-vsn/05668-PTF10cwr/g/"
                   "01-main/0001-img/07-try/qa/spjpeg/"
                   "PTF10cwr_id006852-xg-gsp_spc.jpeg")])
        old_file = self.reference_file_path + "test_case_21.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case22(self):
        """ Test of HLA/HSC extracted grism spectrum. """
        new_str = deliver_data.deliver_data(
            ["hsc_grism"], ["HAG_J033148.83-274850.4_UDFNICP2_V01.SPEC1D.FITS"])
        old_file = self.reference_file_path + "test_case_22.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case23(self):
        """ Test of HLA/HSC 2D grism spectrum - handle it's unsupported. """
        new_str = deliver_data.deliver_data(
            ["hsc_grism"], ["HAG_J033148.83-274850.4_UDFNICP2_V01.SPEC2D.FITS"])
        old_file = self.reference_file_path + "test_case_23.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case24(self):
        """ This uses EPIC 200004923 from Campaign 3. """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2sc"], ["k2sc200004923-c03_lc"], filters=["k2"])
        old_file = self.reference_file_path + "test_case_24.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case25(self):
        """ This uses EPIC 202059070 from Campaign 0. """
        new_str = deliver_data.deliver_data(
            ["hlsp_k2everest"], ["k2everest202059070-c00_lc"], filters=["k2"])
        old_file = self.reference_file_path + "test_case_25.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case26(self):
        """ This tests HSLA support at the coadd level. """
        new_str = deliver_data.deliver_data(
            ["hsla"], ["hsla_coadd"], targets=["NGC-5548"])
        old_file = self.reference_file_path + "test_case_26.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

    def test_case27(self):
        """ This tests HSLA support at the exposure level. """
        new_str = deliver_data.deliver_data(
            ["hsla"], ["lbgu22z3q"], targets=["NGC-5548"])
        old_file = self.reference_file_path + "test_case_27.txt.gz"
        if os.path.isfile(old_file):
            with gzip.open(old_file, 'rb') as oldfile:
                old_str = oldfile.readlines()[0].strip()
        else:
            self.fail(msg="Reference file not found.  Looking for " + old_file)
        self.assertEqual(old_str, new_str)

#--------------------

if __name__ == "__main__":
    unittest.main()

