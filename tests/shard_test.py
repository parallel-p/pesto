import unittest
from shard import shard

class TestShard(unittest.TestCase):
    def test_comon(self):
        arr = {('1', '1'): '1_1\n1_1', ('1', '2'): '1_2', ('2', '1'): '2_1'}
        res = shard(arr, [(lambda x:x[0], lambda x:'c {}'.format(x)), (lambda x:x[1], lambda x:'p {}'.format(x))])
        good = 'c 1:\n\tp 1:\n\t\t1_1\n\t\t1_1\n\tp 2:\n\t\t1_2\nc 2:\n\tp 1:\n\t\t2_1'
        self.assertEqual(res, good)

if __name__ == "__main__":
    unittest.main()
