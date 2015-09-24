#!/usr/bin/python3

import unittest
import os


this_dir = os.path.join(os.path.dirname(__file__), 'tests')
tests = unittest.defaultTestLoader.discover(start_dir=this_dir, pattern='*_test.py')
base = unittest.TestResult()
tests.run(base)
print('RUN - {0}\nERRORS - {1}\nFAILURES - {2}\n'.format(base.testsRun, len(base.errors), len(base.failures)))

if base.failures:
    print('\nFAILURES:\n')
    for failure in base.failures:
        print('\n'.join(map(str, failure)))

if base.errors:
    print('\nERRORS:\n')
    for error in base.errors:
        print('\n'.join(map(str, error)))
