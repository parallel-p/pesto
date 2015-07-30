import unittest
import os


this_dir = os.path.dirname(__file__)
tests = unittest.defaultTestLoader.discover(start_dir=this_dir, pattern='*_test.py')
base = unittest.TestResult()
tests.run(base)
print('RUN - {0}\nERRORS - {1}\nFAILURES - {2}\n'.format(base.testsRun, len(base.errors), len(base.failures)))

if len(base.failures):
    print('\nFAILURES:\n')
    for fail in base.failures:
        for s in fail:
            print(s)

if len(base.errors):
    print('\nERRORS:\n')
    for error in base.errors:
        for s in error:
            print(s)

