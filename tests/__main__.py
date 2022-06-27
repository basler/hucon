"""
Runs all unittests.

Should be executed by `python3 tests/`.
"""
from pathlib import Path
import sys
import unittest

# make modules importable from project dir (e.g. `import webserver`)
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_DIR))

# import all test cases that should be run
from test_hucon_netiface import *

unittest.main()
