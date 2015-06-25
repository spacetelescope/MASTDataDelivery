Commands To Generate Unit Test Reference Files
**********************************************

deliver_data
============

Test Case 01::

```
python deliver_data.py -m kepler -o kplr012644769_lc_Q111111111111111111 > unit_test_reffiles/deliver_data/test_case_01.txt
```
```
gzip unit_test_reffiles/deliver_data/test_case_01.txt
```

Test Case 02::

```
python deliver_data.py -m kepler -o kplr000757450_sc_Q000000000033333300 > unit_test_reffiles/deliver_data/test_case_02.txt
```
```
gzip unit_test_reffiles/deliver_data/test_case_02.txt
```

Test Case 03::

```
python deliver_data.py -m kepler kepler -o kplr012644769_lc_Q111111111111111111 kplr000757450_sc_Q000000000033333300 > unit_test_reffiles/deliver_data/test_case_03.txt
```
```
gzip unit_test_reffiles/deliver_data/test_case_03.txt
```
