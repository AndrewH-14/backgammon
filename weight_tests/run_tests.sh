#!/bin/bash

python3 weight_tests.py  1   0   500 &
python3 weight_tests.py  2  501  1001 &
python3 weight_tests.py  3  1501  2000 &
python3 weight_tests.py  4  2501  3000 &
python3 weight_tests.py  5  3501 4095

wait