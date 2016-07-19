Commands To Generate Unit Test Reference Files
**********************************************

deliver_data
============

Test Case 01::


    python deliver_data.py -m kepler -o kplr012644769_lc_Q111111111111111111 > unit_test_reffiles/deliver_data/test_case_01.txt

    gzip unit_test_reffiles/deliver_data/test_case_01.txt

Test Case 02::

    python deliver_data.py -m kepler -o kplr000757450_sc_Q000000000033333300 > unit_test_reffiles/deliver_data/test_case_02.txt

    gzip unit_test_reffiles/deliver_data/test_case_02.txt

Test Case 03::

    python deliver_data.py -m kepler kepler -o kplr012644769_lc_Q111111111111111111 kplr000757450_sc_Q000000000033333300 > unit_test_reffiles/deliver_data/test_case_03.txt

    gzip unit_test_reffiles/deliver_data/test_case_03.txt

Test Case 04::

    python deliver_data.py -m hlsp_k2varcat -o k2varcat202070161-c00_lc > unit_test_reffiles/deliver_data/test_case_04.txt

    gzip unit_test_reffiles/deliver_data/test_case_04.txt

Test Case 05::

    python deliver_data.py -m hlsp_k2varcat -o k2varcat201515470-c01_lc > unit_test_reffiles/deliver_data/test_case_05.txt

    gzip unit_test_reffiles/deliver_data/test_case_05.txt

Test Case 06::

    python deliver_data.py -m hlsp_k2sff -o k2sff060019819-cet_lc > unit_test_reffiles/deliver_data/test_case_06.txt

    gzip unit_test_reffiles/deliver_data/test_case_06.txt

Test Case 07::

    python deliver_data.py -m hlsp_k2sff -o k2sff202071387-c00_lc > unit_test_reffiles/deliver_data/test_case_07.txt

    gzip unit_test_reffiles/deliver_data/test_case_07.txt

Test Case 08::

    python deliver_data.py -m hlsp_k2sff -o k2sff204417450-c02_lc > unit_test_reffiles/deliver_data/test_case_08.txt

    gzip unit_test_reffiles/deliver_data/test_case_08.txt

Test Case 09::

    python deliver_data.py -m iue -o lwp00501 > unit_test_reffiles/deliver_data/test_case_09.txt

    gzip unit_test_reffiles/deliver_data/test_case_09.txt

Test Case 10::

    python deliver_data.py -m iue -o lwp02572 > unit_test_reffiles/deliver_data/test_case_10.txt

    gzip unit_test_reffiles/deliver_data/test_case_10.txt

Test Case 11::

    python deliver_data.py -m iue -o lwr01244 > unit_test_reffiles/deliver_data/test_case_11.txt

    gzip unit_test_reffiles/deliver_data/test_case_11.txt

Test Case 12::

    python deliver_data.py -m iue -o lwr01245 > unit_test_reffiles/deliver_data/test_case_12.txt

    gzip unit_test_reffiles/deliver_data/test_case_12.txt

Test Case 13::

    python deliver_data.py -m iue -o swp01687 > unit_test_reffiles/deliver_data/test_case_13.txt

    gzip unit_test_reffiles/deliver_data/test_case_13.txt

Test Case 14::

    python deliver_data.py -m iue -o swp01688 > unit_test_reffiles/deliver_data/test_case_14.txt

    gzip unit_test_reffiles/deliver_data/test_case_14.txt

Test Case 15::

    python deliver_data.py -m iue -o lwp04212 > unit_test_reffiles/deliver_data/test_case_15.txt

    gzip unit_test_reffiles/deliver_data/test_case_15.txt

Test Case 16::

    python deliver_data.py -m iue -o lwp15463 > unit_test_reffiles/deliver_data/test_case_16.txt

    gzip unit_test_reffiles/deliver_data/test_case_16.txt

Test Case 17::

    python deliver_data.py -m iue -o swp32470 > unit_test_reffiles/deliver_data/test_case_17.txt

    gzip unit_test_reffiles/deliver_data/test_case_17.txt

Test Case 18::

    python deliver_data.py -m k2 -o ktwo205896873-c03_lc > unit_test_reffiles/deliver_data/test_case_18.txt

    gzip unit_test_reffiles/deliver_data/test_case_18.txt

Test Case 19::

    python deliver_data.py -m galex -o 2518748180271595520 -f NUV -u galex.stsci.edu/data/GR6/pipe/01-vsn/06051-CDFS_00/g/01-main/0001-img/07-try/qa/CDFS_00-xg-int_2color.jpg > unit_test_reffiles/deliver_data/test_case_19.txt

    gzip unit_test_reffiles/deliver_data/test_case_19.txt

Test Case 20::

    python deliver_data.py -m galex -o 2518748180274763038 -f FUV -u galex.stsci.edu/data/GR6/pipe/01-vsn/06051-CDFS_00/g/01-main/0001-img/07-try/qa/spjpeg/CDFS_00_id021790-xg-gsp_spc.jpeg > unit_test_reffiles/deliver_data/test_case_20.txt

    gzip unit_test_reffiles/deliver_data/test_case_20.txt

Test Case 21::

    python deliver_data.py -m galex -o 2505272565762628292 -f NUV -u galex.stsci.edu/data/GR7/pipe/01-vsn/05668-PTF10cwr/g/01-main/0001-img/07-try/qa/spjpeg/PTF10cwr_id006852-xg-gsp_spc.jpeg > unit_test_reffiles/deliver_data/test_case_21.txt

    gzip unit_test_reffiles/deliver_data/test_case_21.txt

Test Case 22::

    python deliver_data.py -m hsc_grism -o HAG_J033148.83-274850.4_UDFNICP2_V01.SPEC1D.FITS > unit_test_reffiles/deliver_data/test_case_22.txt

    gzip unit_test_reffiles/deliver_data/test_case_22.txt

Test Case 23::

    python deliver_data.py -m hsc_grism -o HAG_J033148.83-274850.4_UDFNICP2_V01.SPEC2D.FITS > unit_test_reffiles/deliver_data/test_case_23.txt

    gzip unit_test_reffiles/deliver_data/test_case_23.txt

Test Case 24::

    python deliver_data.py -m hlsp_k2sc -o k2sc200004923-c03_lc > unit_test_reffiles/deliver_data/test_case_24.txt

    gzip unit_test_reffiles/deliver_data/test_case_24.txt

Test Case 25::

    python deliver_data.py -m hlsp_k2everest -o k2everest202059070-c00_lc > unit_test_reffiles/deliver_data/test_case_25.txt

    gzip unit_test_reffiles/deliver_data/test_case_25.txt

