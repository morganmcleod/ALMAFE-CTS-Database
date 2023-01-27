import os
import sys
from os.path import dirname
import unittest

# add the top-level project path to PYTHONPATH:
projectRoot = dirname(dirname(dirname(dirname(__file__))))
if not projectRoot in sys.path:
    sys.path.append(projectRoot)

# and change to that directory:
os.chdir(projectRoot)

from Database.Tests.Unit.CartConfigs import test_CartConfigs
from Database.Tests.Unit.CartTests import test_CartTests
from Database.Tests.Unit.TestTypes import test_TestTypes
from Database.Tests.Unit.MixerTests import test_MixerTests
        
if __name__ == "__main__":
    unittest.main() # run all tests