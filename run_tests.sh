#!/bin/bash

python3 auto.py  1   0     800 &
python3 auto.py  2   801  1600 &
python3 auto.py  3  1601  2400 &
python3 auto.py  4  2401  3200 &
python3 auto.py  5  3201  4000 &
python3 auto.py  6  4001  4800 &
python3 auto.py  7  4801  5600 &
python3 auto.py  8  5600  6560

wait