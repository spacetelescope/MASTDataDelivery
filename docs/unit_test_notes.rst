Commands To Generate Unit Test Reference Files
**********************************************

Prelude
=======
Note: you must run these commands from the root directory of the repo.

deliver_data
============

Test Case 01::

    python -m datadelivery.deliver_data -m kepler -o kplr012644769_lc_Q111111111111111111 -x ../../missions > unit_test_reffiles/deliver_data/test_case_01.txt

    gzip unit_test_reffiles/deliver_data/test_case_01.txt

Test Case 02::

    python -m datadelivery.deliver_data -m kepler -o kplr000757450_sc_Q000000000033333300 -x ../../missions -c ../../missions/kepler/lightcurves/cache > unit_test_reffiles/deliver_data/test_case_02.txt

    gzip unit_test_reffiles/deliver_data/test_case_02.txt

Test Case 03::

    python -m datadelivery.deliver_data -m kepler -o kplr012644769_lc_Q111111111111111111 kplr000757450_sc_Q000000000033333300 -x ../../missions > unit_test_reffiles/deliver_data/test_case_03.txt

    gzip unit_test_reffiles/deliver_data/test_case_03.txt

Test Case 04::

    python -m datadelivery.deliver_data -m hlsp_k2varcat -o k2varcat202070161-c00_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_04.txt

    gzip unit_test_reffiles/deliver_data/test_case_04.txt

Test Case 05::

    python -m datadelivery.deliver_data -m hlsp_k2varcat -o k2varcat201515470-c01_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_05.txt

    gzip unit_test_reffiles/deliver_data/test_case_05.txt

Test Case 06::

    python -m datadelivery.deliver_data -m hlsp_k2sff -o k2sff060019819-cet_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_06.txt

    gzip unit_test_reffiles/deliver_data/test_case_06.txt

Test Case 07::

    python -m datadelivery.deliver_data -m hlsp_k2sff -o k2sff202071387-c00_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_07.txt

    gzip unit_test_reffiles/deliver_data/test_case_07.txt

Test Case 08::

    python -m datadelivery.deliver_data -m hlsp_k2sff -o k2sff204417450-c02_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_08.txt

    gzip unit_test_reffiles/deliver_data/test_case_08.txt

Test Case 09::

    python -m datadelivery.deliver_data -m iue -o lwp00501 -x ../../missions > unit_test_reffiles/deliver_data/test_case_09.txt

    gzip unit_test_reffiles/deliver_data/test_case_09.txt

Test Case 10::

    python -m datadelivery.deliver_data -m iue -o lwp02572 -x ../../missions > unit_test_reffiles/deliver_data/test_case_10.txt

    gzip unit_test_reffiles/deliver_data/test_case_10.txt

Test Case 11::

    python -m datadelivery.deliver_data -m iue -o lwr01244 -x ../../missions > unit_test_reffiles/deliver_data/test_case_11.txt

    gzip unit_test_reffiles/deliver_data/test_case_11.txt

Test Case 12::

    python -m datadelivery.deliver_data -m iue -o lwr01245 -x ../../missions > unit_test_reffiles/deliver_data/test_case_12.txt

    gzip unit_test_reffiles/deliver_data/test_case_12.txt

Test Case 13::

    python -m datadelivery.deliver_data -m iue -o swp01687 -x ../../missions > unit_test_reffiles/deliver_data/test_case_13.txt

    gzip unit_test_reffiles/deliver_data/test_case_13.txt

Test Case 14::

    python -m datadelivery.deliver_data -m iue -o swp01688 -x ../../missions > unit_test_reffiles/deliver_data/test_case_14.txt

    gzip unit_test_reffiles/deliver_data/test_case_14.txt

Test Case 15::

    python -m datadelivery.deliver_data -m iue -o lwp04212 -x ../../missions > unit_test_reffiles/deliver_data/test_case_15.txt

    gzip unit_test_reffiles/deliver_data/test_case_15.txt

Test Case 16::

    python -m datadelivery.deliver_data -m iue -o lwp15463 -x ../../missions > unit_test_reffiles/deliver_data/test_case_16.txt

    gzip unit_test_reffiles/deliver_data/test_case_16.txt

Test Case 17::

    python -m datadelivery.deliver_data -m iue -o swp32470 -x ../../missions > unit_test_reffiles/deliver_data/test_case_17.txt

    gzip unit_test_reffiles/deliver_data/test_case_17.txt

Test Case 18::

    python -m datadelivery.deliver_data -m k2 -o ktwo205896873-c03_lc -x ../../missions > unit_test_reffiles/deliver_data/test_case_18.txt

    gzip unit_test_reffiles/deliver_data/test_case_18.txt

Test Case 19::

    python -m datadelivery.deliver_data -m galex -o 2518748180271595520 -f NUV -u galex.stsci.edu/data/GR6/pipe/01-vsn/06051-CDFS_00/g/01-main/0001-img/07-try/qa/CDFS_00-xg-int_2color.jpg -x ../../missions > unit_test_reffiles/deliver_data/test_case_19.txt

    gzip unit_test_reffiles/deliver_data/test_case_19.txt

Test Case 20::

    python -m datadelivery.deliver_data -m galex -o 2518748180274763038 -f FUV -u galex.stsci.edu/data/GR6/pipe/01-vsn/06051-CDFS_00/g/01-main/0001-img/07-try/qa/spjpeg/CDFS_00_id021790-xg-gsp_spc.jpeg -x ../../missions > unit_test_reffiles/deliver_data/test_case_20.txt

    gzip unit_test_reffiles/deliver_data/test_case_20.txt

Test Case 21::

    python -m datadelivery.deliver_data -m galex -o 2505272565762628292 -f NUV -u galex.stsci.edu/data/GR7/pipe/01-vsn/05668-PTF10cwr/g/01-main/0001-img/07-try/qa/spjpeg/PTF10cwr_id006852-xg-gsp_spc.jpeg -x ../../missions > unit_test_reffiles/deliver_data/test_case_21.txt

    gzip unit_test_reffiles/deliver_data/test_case_21.txt

Test Case 22::

    python -m datadelivery.deliver_data -m hsc_grism -o HAG_J033148.83-274850.4_UDFNICP2_V01.SPEC1D.FITS -x ../../missions > unit_test_reffiles/deliver_data/test_case_22.txt

    gzip unit_test_reffiles/deliver_data/test_case_22.txt

Test Case 23::

    python -m datadelivery.deliver_data -m hsc_grism -o HAG_J033148.83-274850.4_UDFNICP2_V01.SPEC2D.FITS -x ../../missions > unit_test_reffiles/deliver_data/test_case_23.txt

    gzip unit_test_reffiles/deliver_data/test_case_23.txt

Test Case 24::

    python -m datadelivery.deliver_data -m hlsp_k2sc -o k2sc200004923-c03_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_24.txt

    gzip unit_test_reffiles/deliver_data/test_case_24.txt

Test Case 25::

    python -m datadelivery.deliver_data -m hlsp_everest -o everest210636932-c04_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_25.txt

    gzip unit_test_reffiles/deliver_data/test_case_25.txt

Test Case 26::

    python -m datadelivery.deliver_data -m hsla -o hsla_coadd -t NGC-5548 -x ../../missions > unit_test_reffiles/deliver_data/test_case_26.txt

    gzip unit_test_reffiles/deliver_data/test_case_26.txt

Test Case 26_2::

    python -m datadelivery.deliver_data -m hsla -o hsla_coadd -t HD-6655 -x ../../missions > unit_test_reffiles/deliver_data/test_case_26_2.txt

    gzip unit_test_reffiles/deliver_data/test_case_26_2.txt

Test Case 27::

    python -m datadelivery.deliver_data -m hsla -o lbgu22z3q -t NGC-5548 -x ../../missions > unit_test_reffiles/deliver_data/test_case_27.txt

    gzip unit_test_reffiles/deliver_data/test_case_27.txt

Test Case 28::

    python -m datadelivery.deliver_data -m hlsp_polar -o polar201172129-c01_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_28.txt

    gzip unit_test_reffiles/deliver_data/test_case_28.txt

Test Case 29::

    python -m datadelivery.deliver_data -m hlsp_k2gap -o k2gap201121245-c01_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_29.txt

    gzip unit_test_reffiles/deliver_data/test_case_29.txt

Test Case 30::

    python -m datadelivery.deliver_data -m hlsp_kegs -o kegs220163813-c08_lc -y ../../hlsps > unit_test_reffiles/deliver_data/test_case_30.txt

    gzip unit_test_reffiles/deliver_data/test_case_30.txt

Test Case 31::

    python -m datadelivery.deliver_data -m states -o XO-1b_transmission_Deming2013 -s ../../states/ > unit_test_reffiles/deliver_data/test_case_31.txt

    gzip unit_test_reffiles/deliver_data/test_case_31.txt

Test Case 32::

    python -m datadelivery.deliver_data -m states -o TRAPPIST-1b_transmission_deWit2016 -s ../../states/ > unit_test_reffiles/deliver_data/test_case_32.txt

    gzip unit_test_reffiles/deliver_data/test_case_32.txt

Test Case 33::

    python -m datadelivery.deliver_data -m k2 -o ktwo203385347-c15_sc -x ../../missions > unit_test_reffiles/deliver_data/test_case_33.txt

    gzip unit_test_reffiles/deliver_data/test_case_33.txt

Test Case 34::

    python -m datadelivery.deliver_data -m tess -o tess2018234235059-s0002-0000000002733208-0121-s -x ../../missions > unit_test_reffiles/deliver_data/test_case_34.txt

    gzip unit_test_reffiles/deliver_data/test_case_34.txt

Test Case 35::

    python -m datadelivery.deliver_data -m tess -o tess2018263035959-s0003-0000000114434141-0123-s -x ../../missions > unit_test_reffiles/deliver_data/test_case_35.txt

    gzip unit_test_reffiles/deliver_data/test_case_35.txt
