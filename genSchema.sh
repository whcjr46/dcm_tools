#!/bin/bash
wget https://github.com/isb-cgc/examples-Python/raw/master/python/createSchema.py
python createSchema.py $1
rm createSchema.py
